pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'aquagri'
        REGISTRY = 'https://index.docker.io/v1/'
        REGISTRY_CREDENTIALS = '7e28dbbf-3d4b-43b5-afa3-cd5e08cf07e4' // Jenkins credentials ID for Docker Hub
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
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }

        stage('Push to Registry') {
            when {
                expression { return env.REGISTRY != null }
            }
            steps {
                script {
                    docker.withRegistry("${env.REGISTRY}", "${env.REGISTRY_CREDENTIALS}") {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh 'python manage.py migrate'
                        sh 'python manage.py collectstatic --noinput'
                        sh 'gunicorn aquagri.wsgi:application --bind 127.0.0.1:8000'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
