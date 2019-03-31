pipeline {
    agent { docker { image 'python:3-alpine' } }
    stages {
        stage('Git') {
            steps{
                echo 'Getting the code from GitHub...'
                git 'https://github.com/jonbir3/easy_learn_social_network.git'
            }
        }
        stage('Requirements'){
            steps{
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    echo 'Installing Requirements...'
                    sh 'pip3 install --user -r requirements.txt'
                }
            }
        }
        stage('Run Tests'){
            steps{
                echo 'Testing User app...'
                sh "python3 manage.py test users"
            }
        }
        stage('Results') {
            steps{
                echo 'Printing test results...'
                junit '**/nosetests.xml'
            }
        }
    }
}
