"""
    Written by: Pham Ngo Anh Tu
    Date: 2023-12-15 6:00 PM
    Version: 1.0
"""

import uuid
import json

from typing import List
from vul_py_utils.firebase import FirebaseClientWithTask as Firebase
from vul_py_utils.redis import RedisTaskUtil as Redis
from datetime import datetime, timezone
from vul_py_utils.redis.keys import TaskStatus
from vul_py_utils.env_reader import get_str, get_bool
from vul_py_utils.uuid import generate_uuid
from vul_py_utils.pubsub import PubSub
from vul_py_utils.constant import IosUserAgent, AndroidUserAgent
from vul_py_utils.config import (
    ANDROID_FIREBASE_CREDENTIAL_PATH, ANDROID_STORAGE_BUCKET,
    IOS_FIREBASE_CREDENTIAL_PATH, IOS_STORAGE_BUCKET,
    ANDROID_PUBSUB_PROJECT_ID, IOS_PUBSUB_PROJECT_ID,
    PUBSUB_TOPIC_ID, PUBSUB_SUBSCRIPTION_ID,
    REDIS_LOCATION, REDIS_CLUSTER, USE_REDIS, REDIS_TIME_TO_LIVE
)


class ServiceCoordinator():
    """This class is used to interact with all services : Firebase, PubSub, Redis, etc ...
    It will be init in root python path with config for each service.
    If you wish to enable a service, you need to set the environment variable to True. Exp: USE_FIREBASE=True
    
    This class will interact with all services according to the user_agent. Exp: Android or IOS
    Moreover, it will also interact with all services according to the task_id. Exp: task_id = "1234_Android_1234" 
    """

    def __init__(self):
        # FIREBASE
        useFirebase = get_bool("USE_FIREBASE", False)
        if useFirebase:
            self.android_firebase = self.__init_android_firebase_client()
            self.ios_firebase = self.__init_ios_firebase_client()

        # PUBSUB
        usePubSub = get_bool("USE_PUBSUB", False)
        if usePubSub:
            topic = get_str(PUBSUB_TOPIC_ID["key"], PUBSUB_TOPIC_ID["default"])
            subscription_id = get_str(PUBSUB_SUBSCRIPTION_ID["key"], PUBSUB_SUBSCRIPTION_ID["default"])
            self.android_pubsub = self.__init_android_pubsub_client(topic, subscription_id)
            self.ios_pubsub = self.__init_ios_pubsub_client(topic, subscription_id)

        # REDIS
        useRedis = get_bool(USE_REDIS["key"], USE_REDIS["default"])
        redis_url = get_str(REDIS_LOCATION["key"], REDIS_LOCATION["default"])
        redis_cluster_url = get_str(REDIS_CLUSTER["key"], REDIS_CLUSTER["default"])
        ttl = get_str(REDIS_TIME_TO_LIVE["key"], REDIS_TIME_TO_LIVE["default"])
        self.redis_client = Redis(cluster_mode=useRedis, redis_url=redis_url, redis_cluster_nodes=redis_cluster_url, ttl=ttl)

    def get_firebase_by_user_agent(self, user_agent: str) -> Firebase:
        """Get Firebase Client by user_agent

        Args:
            user_agent (str): can be Android or IOS

        Returns:
            Firebase: Firebase client according to user_agent
        """
        if user_agent in AndroidUserAgent:
            return self.android_firebase
        elif user_agent in IosUserAgent:
            return self.ios_firebase

    def get_pubsub_by_user_agent(self, user_agent: str) -> PubSub:
        """Get PubSub Client by user_agent

        Args:
            user_agent (str): can be Android or IOS
        Returns:
            PubSub: PubSub client according to user_agent
        """
        if user_agent in AndroidUserAgent:
            return self.android_pubsub
        elif user_agent in IosUserAgent:
            return self.ios_pubsub

    def init_process(self, firebase: Firebase, device_tokens: List[str], user_id: str = "", body: dict = {}, user_agent: str = "") -> str:
        """This function will init a task with all relating services: PubSub, Firebase, Redis, ...

        Args:
            firebase (Firebase): FireBase client
            device_tokens (List[str]): FCM tokens
            user_id (str)
            body (dict): data you want to send along with the task
            user_agent (str)

        Returns:
            str: task_id
        """
        now = datetime.now(timezone.utc)
        task_id = generate_uuid(user_agent, user_id)
        # Value for Firestore
        body["created_at"] = now.strftime("%Y-%m-%d %H:%M:%S")
        body["id"] = task_id
        firebase.pend_task(task_id, user_id, body)
        # Value for redis
        task_data = {
            "status": TaskStatus.pending.value,
            "device_tokens": " ".join(device_tokens),
            "user_id": user_id,
            "body": json.dumps(body),
            "user_agent": user_agent,
            "result": ""
        }
        self.redis_client.init_task(task_id, task_data)
        return task_id

    def get_task_status_from_firestore(self, user_agent: str, user_id: str, task_id: str) -> dict[str, int]:
        """Fetch task status from Firestore

        Args:
            user_agent (str)
            user_id (str) 
            task_id (str)

        Raises:
            TaskException: raised if task_id not found in firestore

        Returns:
            dict[str,int]: return {"status_code" :  0 pending, 
                                                    1 processing, 
                                                    2 done, 
                                                    3 failed
                                    } 
        """

        firebase = self.get_firebase_by_user_agent(user_agent)
        doc_dict = firebase.get_task(user_id=user_id, task_id=task_id)
        result_dict = {"status": doc_dict["status"],}
        return result_dict

    def get_result_from_firestore(self, user_agent: str, user_id: str, task_id: str) -> dict[str, str]:
        """Fetch result from Firestore

        Args:
            user_agent (str)
            user_id (str) 
            task_id (str)

        Returns:
            dict[str, str]: return task info. If status is not done, return {"status": status_code} 
        """
        firebase = self.get_firebase_by_user_agent(user_agent)
        doc_dict = firebase.get_task(user_id=user_id, task_id=task_id)
        if doc_dict["status"] != TaskStatus.done.value:
            return {"status": doc_dict["status"]}
        else:
            result_dict = {
                "result_url": doc_dict["result_url"],
            }
            return result_dict

    def get_status_from_redis(self, task_id: str) -> dict[str, int]:
        """Fetch status from Redis

        Args:
            task_id (str)

        Raises:
            RedisException: raised if redis is failed

        Returns:
            dict[str,int]: return {"status_code" :  0 pending,
                                                    1 processing, 
                                                    2 done, 
                                                    3 failed
                                    }
        """
        data = self.redis_client.hgetall(task_id)
        data = {key.decode("utf-8"): value for key, value in data.items()}
        if data:
            # Try to get status from redis cache
            task_status = int(data["status"].decode("utf-8"))
            result_dict = {"status": task_status}
            return result_dict
        else:
            return {}

    def get_result_from_redis(self, task_id: str) -> dict[str, str]:
        """Fetch result from Redis

        Args:
            task_id (str)

        Returns:
            dict[str, dict]: return task info. If status is not done, return {"status": status_code}
        """
        data = self.redis_client.hgetall(task_id)
        data = {key.decode("utf-8"): value for key, value in data.items()}
        if data:
            task_status = int(data["status"].decode("utf-8"))
            if task_status == TaskStatus.done.value:
                result_url = str(data["result_url"].decode("utf-8"))
                result_dict = {
                    "result_url": result_url,
                }
                return result_dict
            else:
                return {"status": task_status}
        else:
            return {}

    @staticmethod
    def __init_android_firebase_client() -> Firebase:
        android_key = get_str(ANDROID_FIREBASE_CREDENTIAL_PATH["key"], ANDROID_FIREBASE_CREDENTIAL_PATH["default"])
        android_storage_bucket = get_str(ANDROID_STORAGE_BUCKET["key"], ANDROID_STORAGE_BUCKET["default"])
        return Firebase(android_key, android_storage_bucket, AndroidUserAgent)

    @staticmethod
    def __init_ios_firebase_client() -> Firebase:
        ios_key = get_str(IOS_FIREBASE_CREDENTIAL_PATH["key"], IOS_FIREBASE_CREDENTIAL_PATH["default"])
        ios_storage_bucket = get_str(IOS_STORAGE_BUCKET["key"], IOS_STORAGE_BUCKET["default"])
        return Firebase(ios_key, ios_storage_bucket, IosUserAgent)

    @staticmethod
    def __init_android_pubsub_client(topic: str, subscription_id: str) -> PubSub:
        android_service_account = get_str(ANDROID_FIREBASE_CREDENTIAL_PATH["key"],
                                          ANDROID_FIREBASE_CREDENTIAL_PATH["default"])
        android_project_id = get_str(ANDROID_PUBSUB_PROJECT_ID["key"], ANDROID_PUBSUB_PROJECT_ID["default"])
        return PubSub(android_service_account, android_project_id, topic, subscription_id)

    @staticmethod
    def __init_ios_pubsub_client(topic: str, subscription_id: str) -> PubSub:
        ios_service_account = get_str(IOS_FIREBASE_CREDENTIAL_PATH["key"], IOS_FIREBASE_CREDENTIAL_PATH["default"])
        ios_project_id = get_str(IOS_PUBSUB_PROJECT_ID["key"], IOS_PUBSUB_PROJECT_ID["default"])
        return PubSub(ios_service_account, ios_project_id, topic, subscription_id)
