pipeline {
    agent { label 'agent' }

    stages {
        stage('Checkout') {
            steps {
                // Pulls code from your Git repo
                checkout scm 
            }
        }
    }

stage('Build & Deploy') {
    steps {
        script {
            // 1. COMPLETELY WIPE the corrupted nginx.conf (it's currently a folder)
            sh "rm -rf nginx.conf"
            
            // 2. RESTORE the actual file from your Git repo
            sh "git checkout nginx.conf"
            
            // 3. VERIFY: It must be a FILE (-f), not a directory
            sh 'if [ -d "nginx.conf" ]; then echo "ERROR: nginx.conf is STILL a directory"; exit 1; fi'
            
            // 4. CLEAN UP old containers and volumes to reset the mount state
            sh "docker compose down -v || true"
            
            // 5. RUN: Use --force-recreate to break the bad mount link
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

