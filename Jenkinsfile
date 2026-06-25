pipeline {
    agent any

    environment {
        APP_NAME = 'fintrack'
        BACKEND_IMAGE = 'fintrack-backend'

        // CI-only MySQL sidecar — separate name/port from the dev docker-compose
        // MySQL service so it can never collide with it on the same host.
        CI_MYSQL_CONTAINER = 'fintrack_mysql_ci'
        CI_MYSQL_PORT = '3308'
        CI_MYSQL_ROOT_PASSWORD = 'rootpassword'

        DB_HOST = '127.0.0.1'
        DB_PORT = '3308'
        DB_USER = 'fintrack_user'
        DB_PASSWORD = 'Fintrack@12345'
        DB_NAME = 'fintrack_db'
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

        stage('Start Test Database') {
            steps {
                sh '''
                    # Clean up any leftover container from a previous aborted run
                    docker rm -f ${CI_MYSQL_CONTAINER} || true

                    docker run -d \
                        --name ${CI_MYSQL_CONTAINER} \
                        -e MYSQL_ROOT_PASSWORD=${CI_MYSQL_ROOT_PASSWORD} \
                        -e MYSQL_DATABASE=${DB_NAME} \
                        -e MYSQL_USER=${DB_USER} \
                        -e MYSQL_PASSWORD=${DB_PASSWORD} \
                        -p ${CI_MYSQL_PORT}:3306 \
                        -v ${WORKSPACE}/database/schema.sql:/docker-entrypoint-initdb.d/schema.sql:ro \
                        mysql:8.0

                    echo "Waiting for MySQL to become healthy..."
                    for i in $(seq 1 30); do
                        if docker exec ${CI_MYSQL_CONTAINER} mysqladmin ping -h localhost -uroot -p${CI_MYSQL_ROOT_PASSWORD} --silent; then
                            echo "MySQL is up."
                            break
                        fi
                        if [ "$i" -eq 30 ]; then
                            echo "MySQL did not become healthy in time."
                            docker logs ${CI_MYSQL_CONTAINER} || true
                            exit 1
                        fi
                        sleep 2
                    done
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
                docker rm -f ${CI_MYSQL_CONTAINER} || true
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