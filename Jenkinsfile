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
                bat 'docker build -t my-image .'
            }
        }
        stage('Run Docker Container') {
            steps {
                    // Run the Docker container
                    bat 'docker run -d -p 8080:80 my-image'
            }
        }
    }
}
