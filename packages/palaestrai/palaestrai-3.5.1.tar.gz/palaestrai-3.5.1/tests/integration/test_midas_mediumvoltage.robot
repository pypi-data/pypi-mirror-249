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

*** Test Cases ***
check existig palaestrai modules
    ${py_modules} =                 Run Process     pip  freeze
    Should Contain                  ${py_modules.stdout}   palaestrai
    Should Contain                  ${py_modules.stdout}   palaestrai-environments
    Should Contain                  ${py_modules.stdout}   harl
    Should Contain                  ${py_modules.stdout}   midas-palaestrai
    Should Contain                  ${py_modules.stdout}   midas-mosaik
    Should Contain                  ${py_modules.stdout}   midas-powergrid
    Should Contain                  ${py_modules.stdout}   psi-objectives

midas medium voltage experiment run from a Jupyter Notebook
    START PROCESS                   jupyter  nbconvert    --to    html   --execute   ${CURDIR}${/}midas_integrationtest_palaestrai.ipynb    stdout=${TEMPDIR}${/}stdout.txt     stderr=${TEMPDIR}${/}stderr.txt  alias=arl-integrationtest
    ${result} =                     Wait For Process  handle=arl-integrationtest  timeout=300  on_timeout=kill
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   0
    File Should Exist               ${CURDIR}${/}midas_integrationtest_palaestrai.html

check the existance of agents brain files:
    FOR    ${phase}    IN RANGE    2
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Gandalf SAC (autocurriculum-training)-sac_actor.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Gandalf SAC (autocurriculum-training)-sac_critic.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Gandalf SAC (autocurriculum-training)-sac_actor_target.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Gandalf SAC (autocurriculum-training)-sac_critic_target.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Sauron SAC (autocurriculum-training)-sac_actor.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Sauron SAC (autocurriculum-training)-sac_critic.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Sauron SAC (autocurriculum-training)-sac_actor_target.bin
        File Should Exist               ${CURDIR}${/}_outputs/brains/Classic-ARL-Experiment-0/${phase}/Sauron SAC (autocurriculum-training)-sac_critic_target.bin
    END
    