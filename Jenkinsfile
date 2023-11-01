pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def image = docker.build('fantasy-prem')
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 8084:80 fantasy-prem'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
