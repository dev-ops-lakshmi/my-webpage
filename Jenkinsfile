pipeline {
    agent { label 'agent' }

    stages {
        stage('Cleanup & Checkout') {
            steps {
                script {
                    // 1. Force remove any 'ghost' directories left over from 
                    // previous failed volume mount attempts.
                    sh "if [ -d nginx.conf ]; then rm -rf nginx.conf; fi"
                }
                // 2. Clean the workspace and pull fresh code
                cleanWs()
                checkout scm
            }
        }

        stage('Build & Deploy') {
            steps {
                // 3. Use --build to trigger the Dockerfile.nginx build.
                // This sends your nginx.conf to the Docker daemon automatically.
                sh "docker compose up -d --build --scale ui=3 --scale backend=3"
            }
        }

        stage('Verify') {
            steps {
                sh "docker ps"
                // Check logs to ensure Nginx loaded the baked-in config correctly
                sh "docker compose logs nginx-lb --tail=20"
            }
        }
    }

    post {
        always {
            script {
                // 4. Ensure files are owned by the Jenkins user (UID 1000) 
                // so the agent can delete them next time.
                sh "docker run --rm -v ${env.WORKSPACE}:/ws alpine chown -R 1000:1000 /ws || true"
            }
        }
    }
}
