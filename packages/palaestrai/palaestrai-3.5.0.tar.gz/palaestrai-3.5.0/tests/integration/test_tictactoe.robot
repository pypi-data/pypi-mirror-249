*** Settings ***
Documentation   Run palaestrAI from Jupyter Notebooks
...
...             The Jupyter Notebook kernel is a special environment for
...             palaestrAI to run it. This system test will run
...             jupyter nbconvert --execute for a given iPython notebook in
...             which a palaestrAI experiment is executed.

Library         Process
Library         OperatingSystem
# Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt
    Remove File                     ${CURDIR}${/}tictactoe_integrationtest_palaestrai.html

*** Test Cases ***
check existig palaestrai modules
    ${py_modules} =                 Run Process     pip  freeze
    Should Contain                  ${py_modules.stdout}   palaestrai
    Should Contain                  ${py_modules.stdout}   palaestrai-environments
    Should Contain                  ${py_modules.stdout}   harl

tic-tac-toe experiment run from a Jupyter Notebook  
    ${result} =                     Run Process  jupyter  nbconvert  --to  html  --execute  ${CURDIR}${/}..${/}..${/}doc${/}tutorials${/}01-tic-tac-toe_experiment.ipynb  stdout=${TEMPDIR}${/}stdout.txt  stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   0
    File Should Exist               ${CURDIR}${/}..${/}..${/}doc${/}tutorials${/}01-tic-tac-toe_experiment.html