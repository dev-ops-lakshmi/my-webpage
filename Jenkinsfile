pipeline {
    agent { 
        label 'agent' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm // Pulls code from your Git repo
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    
                    // Build and start services using your docker-compose file
                    // Use --build to ensure fresh images are created
                    docker-compose up --build -d --scale ui=2 --scale backend=2
                }
            }
        }

        stage('Verify') {
            steps {
                // Check if all 5 containers (2 UI, 2 Backend, 1 Nginx) are up
                sh "docker ps"
            }
        }
    }

    post {
        failure {
            // Optional: Clean up on failure
            docker-compose down
        }
    }
}

