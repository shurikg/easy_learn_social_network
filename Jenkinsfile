pipeline {
    agent { docker { image 'python:3-alpine' } }
    stages {
    stage('Git') {
      // Get some code from a GitHub repository
      steps{
          git 'https://github.com/markrity/python-simple-project-example-with-tests.git'
      }
   }
   stage('Requirements'){
          steps{
               withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip3 install --user -r requirements.txt'
               }
          }
    }
    stage('Run Tests'){
          steps{
               sh "nosetests"
          }
    }
    stage('Results') {
       steps{
      junit '**/nosetests.xml'
       }
    }
}
}
