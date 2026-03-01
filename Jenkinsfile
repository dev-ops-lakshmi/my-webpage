pipeline {
    agent { label 'agent' }

    stages {
        stage('Cleanup & Checkout') {
            steps {
                script {
                    // 1. Force remove any "ghost" directories created by failed mounts
                    // If nginx.conf exists as a directory, delete it and restore from Git
                    sh """
                        if [ -d nginx.conf ]; then 
                            echo 'Found directory where file should be. Removing...'
                            rm -rf nginx.conf
                        fi
                    """
                }
                checkout scm
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    // 2. Ensure the host-side Docker daemon can see the file.
                    // This assumes you have mirrored /home/jenkins/workspace 
                    // in your Docker Cloud Plugin 'Mounts' settings.
                    sh "docker compose up --build -d --scale ui=2 --scale backend=2"
                }
            }
        }

        stage('Verify') {
            steps {
                sh "docker ps"
                // Check if Nginx actually started or if it crashed on config
                sh "docker compose logs nginx --tail=20"
            }
        }
    }

    post {
        always {
            script {
                // 3. FIX FOR "Failed to clean the workspace":
                // Change ownership of all files back to the 'jenkins' user (UID 1000)
                // so the Jenkins Agent has permission to delete them.
                sh "docker run --rm -v ${env.WORKSPACE}:/ws alpine chown -R 1000:1000 /ws"
            }
        }
        failure {
            // Optional: Tear down if the deploy fails
            sh "docker compose down --remove-orphans"
        }
    }
}
