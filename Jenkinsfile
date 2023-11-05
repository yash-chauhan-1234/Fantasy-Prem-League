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
                    // Build the Docker image
                    bat 'docker build -t my-image .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the Docker container
                    bat 'docker run -d -p 8501:8501 my-image'
                }
            }
        }
    }

}
