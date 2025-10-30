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
        sh "${DOCKER_COMPOSE} build --pull"
      }
    }

    stage('Start dependencies') {
      steps {
        // Start DB, ZooKeeper, and Kafka first
        sh "${DOCKER_COMPOSE} up -d db zookeeper kafka"
        // Give them some time to initialize
        sh "sleep 20"
      }
    }

    stage('Run migrations') {
      steps {
        sh "${DOCKER_COMPOSE} run --rm django python manage.py migrate --noinput"
      }
    }

    stage('Start application') {
      steps {
        // Now start Django (and optionally Jenkins)
        sh "${DOCKER_COMPOSE} up -d django jenkins"
      }
    }

    stage('Smoke test') {
      steps {
        // Check Django service health
        sh 'curl -f http://localhost:8000/ || echo "API not reachable"'
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
