# Codeforces API Contest.standings

- status

- result

  - contest
    - id
    - name
    - type
    - phase
    - frozen
    - durationSeconds
    - startTimeSeconds
    - relativeTimeSeconds


  - rows
    - penalty
    - rank
    - points
    - party
      - participantType
      - members
      - contestId
      - room
      - ghost
      - startTimeSeconds
    - unsuccessfulHackCount
    - problemResults
      - type
      - points
      - rejectedAttemptCount
      - bestSubmissionTimeSeconds
    - successfulHackCount
  - problems
    - contestId
    - index
    - name
    - type
    - points
    - tags