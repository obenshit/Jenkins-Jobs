pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/obenshit/Jenkins-Jobs.git', credentialsId: 'e042db96-97b5-4eb1-a73d-78999e2c2257'
            }
        }
        stage('Run Python Script') {
            steps {
                sh 'python3 Test_Pipeline_Script.py'
            }
        }
    }
}
