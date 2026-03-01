pipeline {
    agent { label 'agent' }

    options {
        // Stop Jenkins from touching the locked folder before our fix runs
        skipDefaultCheckout(true)
    }

    stages {
        stage('Emergency Host Cleanup') {
            steps {
                script {
                    // 1. We mount the PARENT folder (/home/jenkins) to a container.
                    // This lets us reach "down" and kill the 'workspace' folder which is locked by root.
                    sh "docker run --rm -v /home/jenkins:/parent alpine rm -rf /parent/workspace"
                    
                    // 2. Re-create the workspace folder with correct permissions for the Jenkins user
                    sh "docker run --rm -v /home/jenkins:/parent alpine mkdir -p /parent/workspace"
                    sh "docker run --rm -v /home/jenkins:/parent alpine chown -R 1000:1000 /parent/workspace"
                    
                    // 3. Now the workspace is clean and unlocked on the HOST. 
                    // We can safely checkout and deploy.
                    checkout scm
                    
                    // 4. Ensure nginx.conf is restored as a file
                    sh "if [ -d nginx.conf ]; then rm -rf nginx.conf; fi"
                    sh "git checkout nginx.conf"
                }
            }
        }

        stage('Deploy') {
            steps {
                // Your original compose file with ./nginx.conf mount will now work
                // because the Host and Agent are perfectly synced.
                sh "docker compose up -d --build --scale ui=2 --scale backend=2"
            }
        }
    }

    post {
        always {
            script {
                // Give files back to UID 1000 so Jenkins doesn't crash during post-build cleanup
                sh "docker run --rm -v /home/jenkins/workspace:/ws alpine chown -R 1000:1000 /ws || true"
            }
        }
    }
}
