pipeline {
    agent { label 'agent' }

stages {
        stage('Checkout & Cleanup') {
            steps {
                checkout scm
                script {
                    // Force delete any accidental directories created by previous failed mounts
                    sh 'rm -rf nginx.conf && git checkout nginx.conf'
                    // Stop existing containers to ensure a clean state
                    sh 'docker compose down --remove-orphans || true'
                }
            }
        }

        stage('Update Compose with Sed') {
            steps {
                script {
                    // 1. Get the absolute path of the current workspace
                    // This path MUST exist on the HOST machine for the mount to work
                    def absolutePath = sh(script: 'readlink -f nginx.conf', returnStdout: true).trim()
                    echo "Dynamic Nginx Config Path: ${absolutePath}"

                    // 2. Use sed to replace the placeholder in docker-compose.yml
                    // We use '|' as a delimiter in sed because the path contains slashes '/'
                    sh "sed -i 's|NGINX_CONF_PLACEHOLDER|${absolutePath}|g' docker-compose.yml"
                }
            }
        }

        stage('Deploy & Scale') {
            steps {
                // Now run docker compose with the updated file
                sh "docker compose up -d --build --scale ui=2 --scale backend=2"
            }
        }

        stage('Verify') {
            steps {
                sh "docker ps"
                // Check Nginx logs to see if it actually loaded the config
                sh "docker compose logs nginx | head -n 20"
            }
        }
    }

    post {
        failure {
            // Cleanup on failure to prevent the next run from inheriting the same issue
            sh "docker compose down -v"
        }
    }
}

