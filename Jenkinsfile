pipeline {
    agent {
        label 'agent' // Ensure this matches your Jenkins Node label
    }

    stages {
        stage('Cleanup Environment') {
            steps {
                script {
                    echo "Cleaning up previous runs and corrupted mounts..."
                    // 1. Stop existing containers
                    sh 'docker compose down --remove-orphans || true'
                    
                    // 2. CRITICAL: If 'nginx.conf' was accidentally created as a directory by a failed mount, delete it
                    sh '''
                        if [ -d "nginx.conf" ]; then
                            echo "Deleting corrupted nginx.conf directory..."
                            rm -rf nginx.conf
                        fi
                    '''
                }
            }
        }

        stage('Checkout') {
            steps {
                // Pulls code from your Git repo (contains your .yml, nginx.conf, and Dockerfiles)
                checkout scm 
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    // Verify the file exists before running docker compose
                    sh 'ls -lah nginx.conf' 
                    
                    echo "Starting 2 UI and 2 Backend replicas..."
                    // --build ensures the images are recreated from your latest code
                    sh "docker compose up --build -d --scale ui=2 --scale backend=2"
                }
            }
        }

        stage('Verify Traffic Routing') {
            steps {
                script {
                    echo "Checking container status..."
                    sh "docker ps"
                    
                    echo "Verifying Nginx Logs for upstream routing..."
                    // This shows if Nginx is successfully talking to the 'ui' and 'backend' services
                    sh 'docker compose logs nginx | tail -n 20'
                }
            }
        }
    }

    post {
        success {
            echo "Deployment Successful! Services are scaled and running."
        }
        failure {
            echo "Deployment Failed. Cleaning up..."
            sh "docker compose down"
        }
        always {
            // Optional: Prune unused images to save space on the agent
            sh "docker image prune -f"
        }
    }
}

