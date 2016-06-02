import logging
from src.domain.profile import constants
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.reddit import reddit_client_service

logger = logging.getLogger(__name__)


def get_reddit_profile_attrs(profile_external_id, **kwargs):
  return _get_reddit_profile_data(profile_external_id)


def parse_reddit_submissions(posts):
  return [
    {
      constants.TITLE: post.title, constants.TEXT: post.selftext, 'subreddit': post.subreddit.display_name
    } for post in posts
  ]


def parse_reddit_comments(posts):
  return [{constants.TEXT: post.body, 'subreddit': post.subreddit.display_name} for post in posts]


def _get_reddit_profile_data(profile_external_id, _reddit_client_service=None):
  if not _reddit_client_service: _reddit_client_service = reddit_client_service

  log_message = (
    "Get reddit profile data. reddit_id: %s",
    profile_external_id
  )

  with log_wrapper(logger.debug, *log_message):
    user = _reddit_client_service.search_by_redditor(profile_external_id)

    profile_url = user._url
    name = user.name

    recent_comments = user.get_comments(limit=5)
    recent_comments = parse_reddit_comments(recent_comments)

    recent_submissions = user.get_submitted(limit=5)
    recent_submissions = parse_reddit_submissions(recent_submissions)

    reddit_profile_data = {
      constants.PROFILE_URL: profile_url,
      constants.NAME: name,
      constants.RECENT_COMMENTS: recent_comments,
      constants.RECENT_SUBMISSIONS: recent_submissions,
    }

  return reddit_profile_data
