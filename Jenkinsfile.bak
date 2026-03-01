pipeline {
    agent { label 'agent' }

    options {
        // CRITICAL: Stop Jenkins from trying to clean the workspace 
        // with the Git plugin, which is failing due to root permissions.
        skipDefaultCheckout(true)
    }

    stages {
        stage('Manual Clean & Checkout') {
            steps {
                script {
                    // 1. Use a root-level Docker container to fix permissions on the host path.
                    // This 'chowns' everything to UID 1000 so Jenkins can handle the files.
                    sh "docker run --rm -v ${env.WORKSPACE}:/ws alpine chown -R 1000:1000 /ws || true"
                    
                    // 2. Now clean the workspace safely
                    cleanWs()
                    
                    // 3. Manually perform the checkout now that the space is clean
                    checkout scm
                    
                    // 4. Final safety check: remove 'nginx.conf' if it was left as a directory
                    sh "if [ -d nginx.conf ]; then rm -rf nginx.conf; fi"
                    sh "git checkout nginx.conf"
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                // Ensure --build is used to bake the nginx.conf into the container image
                sh "docker compose up --build -d --scale ui=2 --scale backend=2"
            }
        }

        stage('Verify') {
            steps {
                sh "docker ps"
                sh "docker compose logs nginx --tail=20"
            }
        }
    }

    post {
        always {
            script {
                // Fix permissions AGAIN at the end so the NEXT build doesn't fail at the start.
                sh "docker run --rm -v ${env.WORKSPACE}:/ws alpine chown -R 1000:1000 /ws || true"
            }
        }
    }
}
