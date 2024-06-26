| *** Settings ***  |                                              |
| Library           | RequestsLibrary                              |
| Library           | Collections                                  |
| Library           | OperatingSystem                              |
| Library           | String                                       |
| Library           | Process                                      |
| Resource          | ./rag_app_test_data.robot                    |


*** Test Cases ***
| RagTestCase1        | [Tags]           | Rag                 |                              |              |
|                     | ${test_1}        | Get File            | ${test_1}                    |              |
|                     | ${body}          | Evaluate            | json.loads(r'''${test_1}''') |              |
|                     | ${resp}          | POST                | ${app_url}                   | json=${body} |
|                     | Status Should Be | OK                  | ${resp}                      |              |
|                     | ${resp}          | Set Variable        | ${resp.json()}               |              |
|                     | Log To Console   | ${resp}             |                              |              |
|                     | ${answer}        | Get From Dictionary | ${resp}                      | answer       |
|                     | Should Contain   | ${answer}           | ${check_1_1}                 |              |

*** Test Cases ***
| RagTestCase2        | [Tags]           | Rag                 |                              |              |
|                     | ${test_1}        | Get File            | ${test_2}                    |              |
|                     | ${body}          | Evaluate            | json.loads(r'''${test_1}''') |              |
|                     | ${resp}          | POST                | ${app_url}                   | json=${body} |
|                     | Status Should Be | OK                  | ${resp}                      |              |
|                     | ${resp}          | Set Variable        | ${resp.json()}               |              |
|                     | Log To Console   | ${resp}             |                              |              |
|                     | ${answer}        | Get From Dictionary | ${resp}                      | answer       |
|                     | Should Contain   | ${answer}           | ${check_2_1}                 |              |
|                     | Should Contain   | ${answer}           | ${check_2_2}                 |              |
|                     | Should Contain   | ${answer}           | ${check_2_3}                 |              |
|                     | Should Contain   | ${answer}           | ${check_2_4}                 |              |
