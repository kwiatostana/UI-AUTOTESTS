pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create .env') {
            steps {
                withCredentials([file(credentialsId: 'env-file', variable: 'ENV_FILE')]) {
                    bat 'copy %ENV_FILE% .env'
                }
            }
        }

        stage('Pull Browser Images') {
            steps {
                bat 'docker pull selenoid/chrome:128.0'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'docker-compose up --build --abort-on-container-exit --exit-code-from tests'
            }
        }
    }

    post {
        always {
            bat 'docker-compose down'
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
    }
}
