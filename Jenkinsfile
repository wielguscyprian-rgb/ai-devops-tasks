pipeline {
    agent any

    environment {
        REGISTRY_HOST        = 'docker.io'
        IMAGE_NAME           = 'moje-konto/node-app'
        IMAGE_TAG            = "${BUILD_NUMBER}"
        REGISTRY_CREDENTIALS = 'docker-hub-credentials' // ID danych uwierzytelniających zdefiniowane w Jenkinsie
    }

    tools {
        // Wymaga zainstalowanego i skonfigurowanego "NodeJS Plugin" w Jenkinsie
        nodejs 'NodeJS-18' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Pobiera kod z repozytorium podłączonego do tego pipeline
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // 'npm ci' zapewnia spójną instalację na podstawie package-lock.json
                sh 'npm ci'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'npm test'
            }
        }

        stage('Build Application') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Budowanie obrazu z wykorzystaniem oficjalnego pluginu Docker Pipeline
                    dockerImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Publish Docker Image') {
            steps {
                script {
                    // Logowanie do rejestru i wysyłanie obrazów z tagami numeru buildu i latest
                    docker.withRegistry("https://${REGISTRY_HOST}", REGISTRY_CREDENTIALS) {
                        dockerImage.push("${IMAGE_TAG}")
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }

    post {
        always {
            // Czyszczenie przestrzeni roboczej po zakończeniu wykonania
            cleanWs()
        }
        success {
            echo "Pipeline zakończony sukcesem. Obraz ${IMAGE_NAME}:${IMAGE_TAG} został opublikowany."
        }
        failure {
            echo "Pipeline zakończony niepowodzeniem."
        }
    }
}