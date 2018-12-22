Feature: Add a listen to a playlist
  Scenario: A playlist doesn't exist for the listen's submit date
    Given a listen has just been created with the fields
      | id | song_id                | listen_time_utc            | song_provider |
      |  1 | 41wel0JyLABRedko4XZLG1 | 2018-12-22T00:00:05.987156 | SPOTIFY       |
    And a playlist doesn't exist for "2018-12-22"
    When playlists receives an add-listen-to-playlist message
    Then there is a playlist for "2018-12-22"
    And the song id "41wel0JyLABRedko4XZLG1" has been added to the corresponding spotify playlist

  Scenario: A playlist exists for the listen's submit date, and the listen hasn't been submitted
    Given a listen has just been created with the fields
      | id | song_id                | listen_time_utc            | song_provider |
      |  2 | 0kJ4CyjZJT0P4caqKYG4jZ | 2018-12-22T10:30:05.252424 | SPOTIFY       |
    And a playlist exists for "2018-12-22"
    And the spotify playlist has the tracks
      | song_id                |
      | 41wel0JyLABRedko4XZLG1 |
    When playlists receives an add-listen-to-playlist message
    Then there is a playlist for "2018-12-22"
    And the song id "0kJ4CyjZJT0P4caqKYG4jZ" has been added to the corresponding spotify playlist


  Scenario: A playlist exists for the listen's submit date, and the listen has already been submitted
    Given a listen has just been created with the fields
      | id | song_id                | listen_time_utc            | song_provider |
      |  3 | 41wel0JyLABRedko4XZLG1 | 2018-12-22T14:15:05.000002 | SPOTIFY       |
    And a playlist exists for "2018-12-22"
    And the spotify playlist has the tracks
      | song_id                |
      | 41wel0JyLABRedko4XZLG1 |
      | 0kJ4CyjZJT0P4caqKYG4jZ |
    When playlists receives an add-listen-to-playlist message
    Then there is a playlist for "2018-12-22"
    And the song id "0kJ4CyjZJT0P4caqKYG4jZ" has not been added to the corresponding spotify playlist
