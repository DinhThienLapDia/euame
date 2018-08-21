from stream_django.enrich import Enrich as BaseEnrich
from api.models import Friend
from api.models import Feed


def did_i_feed_items(user, items):
    feedned_items_ids = user.feed_set.filter(item_id__in=items, deleted_at__isnull=True).values_list('item_id', flat=True)
    for item in items:
        item.feedned = item.id in feedned_items_ids


def did_i_feed(user, feeds):
    did_i_feed_items(user, [feed.item for feed in feeds])


def do_i_friend_users(user, users):
    friended_user_ids = Friend.objects.filter(user_id=user.id, target__in=users, deleted_at__isnull=True).values_list('target_id', flat=True)
    for u in users:
        u.friended = u.id in friended_user_ids


def do_i_friend(user, friends):
    do_i_friend_users(user, [f.target for f in friends])


class Enrich(BaseEnrich):

    def __init__(self, current_user, *args, **kwargs):
        super(Enrich, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def fetch_feed_instances(self, pks):
        feeds = Feed.objects.select_related(*feed.activity_related_models()).in_bulk(pks)
        if self.current_user.is_authenticated():
            did_i_feed(self.current_user, feeds.values())
        return feeds

    def fetch_friend_instances(self, pks):
        friends = Friend.objects.select_related(*friend.activity_related_models()).in_bulk(pks)
        if self.current_user.is_authenticated():
            do_i_friend(self.current_user, friends.values())
        return friends