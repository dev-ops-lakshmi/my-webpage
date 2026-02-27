pipeline {
    agent { label 'agent' }

    stages {
        stage('Checkout') {
            steps {
                // Pulls code from your Git repo
                checkout scm 
            }
        }

        stage('Fix Mounts & Deploy') {
            steps {
                script {
                    // 1. DELETE THE FAKE DIRECTORY: Docker creates this if the file was missing
                    // Run this EVERY time to ensure the host is clean
                    sh 'rm -rf nginx.conf'
                    
                    // 2. FORCE RESTORE: Ensure the actual file from Git is present
                    sh 'git checkout nginx.conf'
                    
                    // 3. VERIFY: Confirm it is a file (not a directory) before launching
                    sh '[ -f nginx.conf ] || (echo "ERROR: nginx.conf is missing or still a directory" && exit 1)'

                    // 4. DEPLOY: Using --force-recreate ensures no stale volume data remains
                    sh "docker compose up --build -d --force-recreate --scale ui=2 --scale backend=2"
                }
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

