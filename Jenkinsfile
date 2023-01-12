pipeline {
    agent any
  
    stages {
        stage('Source') {
            steps {
                // Get  code from a GitHub repository
                git 'https://github.com/mdjawad0/Django-BankingApp-Deployment.git'
                
                echo 'Source Stage Finished'
            }
        }

        stage('Test') {
            steps {
                withPythonEnv('/home/pritithadanisim/Documents/banking-env/') {
                    // Print Path for Environment
                    sh "pip -V"
                    
                    // Run  test command
                    sh "python manage.py test"
                }
                
                echo 'Test Stage Finished'
            }
        }

        stage('Deploy') {
            steps {
        
             withPythonEnv('/home/pritithadanisim/Documents/banking-env/') {
                // Run The Command to Start the  Server
                sh "python manage.py runserver 0:8000"
                echo 'Deploy Stage Finished'
             }

            }
        }
    }
}
