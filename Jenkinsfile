pipeline {
  agent any

  environment {
    DOCKER_COMPOSE = 'docker compose'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build images') {
      steps {
        bat "${DOCKER_COMPOSE} build --pull"
      }
    }

    stage('Start dependencies') {
      steps {
        // Start DB, ZooKeeper, and Kafka first
        bat "${DOCKER_COMPOSE} up -d db zookeeper kafka"
        // Give them some time to initialize
        // bat "sleep 20"
        echo '⏳ Waiting for dependencies to initialize...'
        bat 'powershell -Command "Start-Sleep -Seconds 20"'
      }
    }

    stage('Run migrations') {
      steps {
        bat "${DOCKER_COMPOSE} run --rm django python manage.py migrate --noinput"
      }
    }

    stage('Start application') {
      steps {
        // Now start Django (and optionally Jenkins)
        bat "${DOCKER_COMPOSE} up -d django"
      }
    }

    stage('Smoke test') {
      steps {
        echo '⏳ Waiting for Django to become ready...'
        bat 'powershell -Command "Start-Sleep -Seconds 15"'
        bat 'curl -f http://localhost:8000/api/log/ || echo "API not reachable"'
      }
    }
  }

  post {
    success {
      echo "✅ Pipeline completed successfully."
    }
    failure {
      echo "❌ Pipeline failed."
    }
  }
}
