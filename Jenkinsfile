pipeline {
    agent { label 'agent' }

    stages {
        stage('Cleanup & Checkout') {
            steps {
                script {
                    // 1. Force remove any 'ghost' directories
                    sh "if [ -d nginx.conf ]; then rm -rf nginx.conf; fi"
                }
                // 2. Clean the workspace and pull fresh code
                cleanWs()
                checkout scm
            }
        }

        stage('Build & Deploy') {
            steps {
                // 3. Trigger the Dockerfile.nginx build
                sh "docker compose up -d --build --scale ui=3 --scale backend=3"
            }
        }

        stage('Verify') {
            steps {
                sh "docker ps"
                // Check logs to ensure Nginx loaded the config correctly
                sh "docker compose logs nginx-lb --tail=20"
            }
        }
    }

    post {
        always {
            script {
                // 4. Ensure files are owned by the Jenkins user for next time
                sh "docker run --rm -v ${env.WORKSPACE}:/ws alpine chown -R 1000:1000 /ws || true"
            }
        }
        success {
            // Sends email only if the build finishes successfully
            mail to: 'lakshmitalks10@gmail.com',
                 subject: "SUCCESS: Job '${env.JOB_NAME}' [${env.BUILD_NUMBER}]",
                 body: "The build was successful! You can view the details here: ${env.BUILD_URL}"
        }
        failure {
            // Sends email only if the build fails
            mail to: 'lakshmitalks10@gmail.com',
                 subject: "FAILED: Job '${env.JOB_NAME}' [${env.BUILD_NUMBER}]",
                 body: "The build failed. Please check the console logs: ${env.BUILD_URL}console"
        }
    }
}
