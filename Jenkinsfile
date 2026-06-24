pipeline {
    agent any

    environment {
        APP_NAME = 'fintrack'
        BACKEND_IMAGE = 'fintrack-backend'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Show Environment') {
            steps {
                sh '''
                    echo "Workspace: $WORKSPACE"
                    git --version
                    python3 --version || true
                    docker --version
                '''
            }
        }

        stage('Install Test Dependencies') {
            steps {
                sh '''
                    cd backend
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . backend/venv/bin/activate
                    pytest tests
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${BACKEND_IMAGE}:latest backend
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker images | grep ${BACKEND_IMAGE} || true
            '''
        }

        success {
            echo 'FinTrack CI pipeline completed successfully.'
        }

        failure {
            echo 'FinTrack CI pipeline failed. Check the Jenkins console output.'
        }
    }
}