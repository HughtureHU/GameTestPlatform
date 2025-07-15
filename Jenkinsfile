// Jenkinsfile - Final Professional Version
pipeline {
    agent { label 'windows' } 

    stages {
        stage('Setup Workspace & Build Game') {
            steps {
                // dir 步骤可以让我们后续所有的bat命令都在'backend'这个子目录里执行
                dir('backend') {
                    
                    // 第1步: 打印当前工作目录，用于调试
                    echo "--- Current working directory is now inside 'backend' folder ---"
                    bat 'cd'

                    // 第2步: 动态创建一个全新的、干净的虚拟环境
                    echo "--- Creating a fresh Python virtual environment... ---"
                    bat 'python -m venv venv'

                    // 第3步: 激活新环境，并安装所有必需的Python库
                    echo "--- Installing required Python packages... ---"
                    bat 'call .\\venv\\Scripts\\activate.bat && pip install "fastapi[all]" requests'

                    // 第4步: 在准备好的环境中，执行真正的游戏打包脚本
                    echo "--- Starting the game build script... ---"
                    bat 'call .\\venv\\Scripts\\activate.bat && python scripts\\build_lyra.py'
                }
            }
        }
    }

    post {
        always {
            echo '--- Pipeline finished. ---'
        }
    }
}