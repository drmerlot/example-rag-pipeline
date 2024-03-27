| *** Settings ***  |                                              |
| Library           | RequestsLibrary                              |
| Library           | Collections                                  |
| Library           | OperatingSystem                              |
| Library           | String                                       |
| Library           | Process                                      |
| Resource          | ./rag_app_test_data.robot     |


*** Test Cases ***
| RagTestCase1     | [Tags]           | Rag          |                              |              |
|                     | ${test_1}        | Get File            | ${test_1}                    |              |
|                     | ${body}          | Evaluate            | json.loads(r'''${test_1}''') |              |
|                     | ${resp}          | POST                | ${app_url}           | json=${body} |
|                     | Status Should Be | OK                  | ${resp}                      |              |
|                     | ${resp}          | Set Variable        | ${resp.json()}               |              |
|                     | Log To Console   | ${resp}             |                              |              |
|                     | ${room}          | Get From Dictionary | ${resp}                      | room         |
|                     | ${room_0}        | Get From List       | ${room}                      | 0            |
|                     | ${uuid}          | Get From Dictionary | ${room_0}                    | uuid         |
|                     | ${name}          | Get From Dictionary | ${room_0}                    | name         |
|                     | Should Be Equal  | ${name}             | ${check_1_1}                 |              |
|                     | Should Be Equal  | ${uuid}             | ${check_1_2}