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
                bat 'docker-compose up --build -d'
            }
        } 
    }
}
