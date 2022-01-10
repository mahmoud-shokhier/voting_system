# voting_system APIs
Voter Registration
  ○ The voter is registered by providing the following information:
    ■ email
    ■ password
    ■ name
  ○ A user cannot use a previously registered email.

Login
  ○ The user logs in using their email and password.
  ○ The response should include an access token that should be used to
  authenticate the below endpoints.
  ○ The access token should expire after 10 minutes.
  ○ The endpoint should also return a refresh token that can be used to generate a
  new access token, without the user having to login again after the authentication
  token has expired.
  ○ The refresh token should expire after 1 hour.

Refresh
  ○ Receives the user’s refresh token, and creates another pair of tokens (access
  token and refresh token)

Get Polls
  ○ Fetches all the system’s polls, with their respective choices, poll results (number
  of votes for each choice), and each poll’s status, whether it is expired or not.
  ○ The user can search for a specific poll using a search term. The term should be
  searched for in the poll’s title, description or one of its choices.
  ○ Polls should be ordered by expiry date & time, where the polls with the latest
  expiry are displayed first.
  ○ Response data should be paginated (page size and page number to be provided
  by the user)

Vote Poll
  ○ The user votes on a poll by selecting one of the choices, only if the poll has not
  expired, and if the user has not cast a vote on this poll before.
  
Implement Token authentication (Including models, views & business logic) functionalities without relying on DRF or other third-party libraries:
  
