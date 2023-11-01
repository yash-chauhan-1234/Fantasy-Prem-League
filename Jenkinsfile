pipeline {
    agent any

    environment {
        PATH = "C:\\WINDOWS\\SYSTEM32"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    bat 'docker build -t my-image .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the Docker container
                    bat 'docker run -d -p 8084:80 my-image'
                }
            }
        }
    }

    post {
        always {
            // Cleanup: Stop and remove the container
            bat 'docker stop my-container || true'
            bat 'docker rm my-container || true'
        }
    }
}
