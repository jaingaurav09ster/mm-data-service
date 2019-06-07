#!groovy

library identifier: 'devops-shared-library@master', retriever: modernSCM([$class: 'GitSCMSource',
	remote: 'https://github.lbg.eu-gb.bluemix.net/POC77-MachineLearning/devops-shared-library.git',
	credentialsId: 'jenkinsGHEPAT'])

pipeline {
        options {
            buildDiscarder(logRotator(artifactDaysToKeepStr: '30', artifactNumToKeepStr: '5', daysToKeepStr: '30', numToKeepStr: '5'))
        }
        environment{
            GITHUB_USER = 'POC77-MachineLearning'
            PROJECT_NAME = 'mm-data-visualisation'
        }
        agent {
            kubernetes {
                label "ds-python-${UUID.randomUUID().toString()}"
                yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: jenkins-pipeline
spec:
  containers:
  - name: jnlp
    image: registry-proxy.lbg.eu-gb.mybluemix.net/mm-mlp/jnlp-slave:3.23-1-alpine
    ttyEnabled: true
  - name: python
    image: registry-proxy.lbg.eu-gb.mybluemix.net/modelmaker/infra/miniconda-with-dev-tools:4.5.4
    command:
    - cat
    tty: true
  - name: sonar-scanner
    image: registry-proxy.lbg.eu-gb.mybluemix.net/sonar-scanner-python:3.2.0.1227
    command:
    - cat
    tty: true
  - name: java
    image: registry-proxy.lbg.eu-gb.mybluemix.net/java:8
    command:
    - cat
    tty: true
"""
            }
        }
        stages {
            stage('Install Requirements') {
                steps {
                    container('python') {
                        installDependencies(archeType: 'python', dependenciesFile: 'requirements.txt,tests/requirements.txt')
                    }
                }
            }
            
            stage('Code Analysis') {
                parallel {
                    stage('Unit Tests') {
                        steps {
                            container('python') {
                                runUnitTests(archeType: 'python', outputFile: 'pyTests.xml', allureDir: 'allure-results')
                            }
                        }
                    }

                    stage('Sonar Scanner') {
                        steps {
                            container('sonar-scanner') {
                                echo 'Running sonar scan'
                                runSonarScanner(archeType: 'python',
                                    outputFile: 'pyTests.xml',
                                    source: 'mm_shared_utils',
                                    tests: 'tests',
                                    projectKey: 'com.lbg.mip.ds-python-common-utils',
                                    hostURL: 'http://sonar.sandbox.extranet.group/sonar',
                                    projectName: env.PROJECT_NAME,
                                    branch: env.BRANCH_NAME,
                                    projectVersion: env.BUILD_NUMBER )
                            }
                        }
                    }
                }
            }

            stage('Package') {
                when{
                    branch 'master'
                }
                steps {
                    container('python') {
                        sh '''
                            git config --global user.email "tpf.jenkins@lloydsbanking.com"
                            git config --global user.name "tpfsavings jenkins"
                        '''
                        echo 'Generating the distribution'
                        runPackaging(archeType: 'python')
                    }
                }
            }

            stage('Deploy') {
                when{
                    branch 'master'
                }
                environment {
                    NEXUS_ACCESS = credentials('nexus-uploader')
                    GITHUB_URL = 'github.lbg.eu-gb.bluemix.net/${GITHUB_USER}/${PROJECT_NAME}.git'
                    GITHUB_ACCESS = credentials('jenkinsGHEPAT')
                }
                steps {
                    container('python') {
                        echo 'Deploy package to nexus.'
                        nexusDeployer(archeType: 'python', username: env.NEXUS_ACCESS_USR, password: env.NEXUS_ACCESS_PSW, srcDir: 'dist/*', gitUrl: env.GITHUB_URL, gitCreds: env.GITHUB_ACCESS)
                    }
                }
            }

            stage('Publish') {
                steps {
                    container('java') {
                        echo 'Generating allure reports'
                        generateAllureReport(resultPath: 'allure-results')
                    }
                }
            }
        }
    }
