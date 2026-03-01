pipeline {
    agent { label 'agent' }

    options {
        // Prevents the "Failed to clean workspace" error on start
        skipDefaultCheckout(true)
    }

    stages {
        stage('Dynamic Host Cleanup') {
            steps {
                script {
                    // 1. Force-delete the workspace folder ON THE HOST VM using a root container.
                    // This clears the "ghost" directories (nginx.conf) and root-owned files.
                    // We mount the parent folder so we can wipe the current workspace folder completely.
                    sh "docker run --rm -v /home/jenkins/workspace:/parent alpine rm -rf /parent/${env.JOB_BASE_NAME}"
                    
                    // 2. Now that the Host is clean, the Agent can safely clean its internal view
                    cleanWs()
                    
                    // 3. Pull fresh code
                    checkout scm
                    
                    // 4. Double check nginx.conf is a file, not a directory
                    sh "if [ -d nginx.conf ]; then rm -rf nginx.conf; fi"
                    sh "git checkout nginx.conf"
                }
            }
        }

        stage('Deploy') {
            steps {
                // Now the Host and Agent are perfectly synced. 
                // The Host will see ./nginx.conf as a file.
                sh "docker compose up -d --build --scale ui=2 --scale backend=2"
            }
        }
    }

    post {
        always {
            script {
                // Final fix: give files back to Jenkins user so 'post' steps don't fail
                sh "docker run --rm -v ${env.WORKSPACE}:/ws alpine chown -R 1000:1000 /ws || true"
            }
        }
    }
}
