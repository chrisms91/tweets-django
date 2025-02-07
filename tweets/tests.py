from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from . import models
from users.models import User


class TestTweets(APITestCase):

    def setUp(self):
        test_user = User.objects.create(username="test_user")
        test_user.set_password("123")
        test_user.save()
        self.user = test_user

        models.Tweet.objects.create(payload="test payload", user=test_user)

    def test_get_tweets_valid(self):
        res = self.client.get("/api/v1/tweets/")
        self.assertEqual(res.status_code, HTTP_200_OK)

        data = res.json()
        self.assertEqual(data[0]["payload"], "test payload")

    def test_post_tweets_valid(self):
        self.client.force_login(self.user)
        new_payload = "new payload"
        res = self.client.post("/api/v1/tweets/", data={"payload": new_payload})
        self.assertEqual(res.status_code, HTTP_200_OK)

        data = res.json()
        self.assertEqual(data["user"]["username"], "test_user")
        self.assertEqual(data["payload"], new_payload)

    def test_post_tweets_invalid(self):
        new_payload = "new payload"
        res = self.client.post(
            "/api/v1/tweets/", data={"payload": new_payload}
        )  # user not logged in
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

        self.client.force_login(self.user)
        res = self.client.post("/api/v1/tweets/", data={})  # empty data
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

        invalid_payload = "t" * 181
        res = self.client.post(
            "/api/v1/tweets/", data={"payload": invalid_payload}
        )  # too long
        self.assertIn("payload", res.json())
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)


class TwetTweetDetail(APITestCase):
    def setUp(self):
        test_user = User.objects.create(username="test_user")
        test_user.set_password("123")
        test_user.save()
        self.user = test_user

        models.Tweet.objects.create(payload="test payload", user=test_user)

    def test_get_tweet_detail_valid(self):
        res = self.client.get("/api/v1/tweets/1")
        self.assertEqual(res.status_code, HTTP_200_OK)

        data = res.json()
        self.assertEqual(data["id"], 1)

    def test_get_tweet_detail_not_found(self):
        res = self.client.get("/api/v1/tweets/3")
        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)

    def test_put_tweet_detail_valid(self):
        self.client.force_login(self.user)
        updated_payload = "updated payload"
        res = self.client.put("/api/v1/tweets/1", data={"payload": updated_payload})
        self.assertEqual(res.status_code, HTTP_200_OK)

        data = res.json()
        self.assertEqual(data["payload"], updated_payload)

    def test_put_tweet_detail_invalid(self):
        updated_payload = "updated payload"
        res = self.client.put(
            "/api/v1/tweets/1", data={"payload": updated_payload}
        )  # user not logged in
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

        self.client.force_login(self.user)
        invalid_payload = "t" * 181
        res = self.client.put(
            "/api/v1/tweets/1", data={"payload": invalid_payload}
        )  # too long
        self.assertIn("payload", res.json())
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_delete_tweet_detail_valid(self):
        self.client.force_login(self.user)
        res = self.client.delete("/api/v1/tweets/1")
        self.assertEqual(res.status_code, HTTP_200_OK)

    def test_delete_tweet_detail_not_found(self):
        self.client.force_login(self.user)
        res = self.client.delete("/api/v1/tweets/5")
        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)
