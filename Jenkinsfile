pipeline {
    agent any
    stages {
        stage('Initialize') {
            steps {
                script {
                    // Variables para detectar cambios
                    env.MICROSERVICE_CHANGED = 'true'
                    env.MODEL_TRAINING_CHANGED = 'false'

                    // Obtener la lista de archivos modificados utilizando git
                    def changes = sh(script: "git diff --name-only HEAD~1 HEAD", returnStdout: true).trim().split("\n")

                    // Verificar si se han realizado cambios en modelsserver o model
                    changes.each { change ->
                        if (change.startsWith('model_server/') || change.startsWith('Jenkins')) {
                            env.MICROSERVICE_CHANGED = 'true'
                        }
                        if (change.startsWith('model/') || change.startsWith('Jenkins'))  {
                            env.MODEL_TRAINING_CHANGED = 'false'
                        }
                    }
                }
            }
        }

        stage('Microservice Build') {
            when {
                expression { return env.MICROSERVICE_CHANGED == 'true' }
            }
            steps {
                script {
                    buildMicroservice()
                }
            }
        }

        stage('Model Training') {
            when {
                expression { return env.MODEL_TRAINING_CHANGED == 'true' }
            }
            steps {
                script {
                    trainModel()
                }
            }
        }
    }
}

def buildMicroservice() {
    dir('model_server') {
        // Levantando venv
        sh 'chmod +x ./setup_model_server.sh'
        sh 'chmod +x ./setup_cloud.sh'
        sh './setup_model_server.sh'

        def pytestResult = sh(script: './venv/bin/pytest --junitxml=report.xml', returnStatus: true)
        // Verificando el estado de salida de pytest
        if (pytestResult == 0) {
            echo 'Las pruebas de pytest pasaron, desplegando a Cloud Run'
            // Ejecutando el comando de gcloud solo si las pruebas de pytest pasan
            sh './setup_cloud.sh'
        } else {
            echo 'Las pruebas de pytest fallaron, el despliegue a Cloud Run se va a omitir'
        }

        echo 'Limpiando entorno virtual'
        sh 'rm -rf venv'            
    }
}


def trainModel() {
    dir('model') {
        // Procesamiento y fit del modelo
        sh 'chmod +x ./setup_model.sh'
        sh './setup_model.sh'
    }
}