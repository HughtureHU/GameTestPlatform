import os
import subprocess
import sys

UE_ENGINE_PATH = "F:/UE5/UEVERSION/UE_5.5"
LYRA_PROJECT_PATH = "F:/UE5/pro/LyraStarterGame/LyraStarterGame.uproject"
PACKAGE_OUTPUT_PATH = "F:/UE5/OUTPUT"


def main():
    """
    主函数，执行Lyra项目的自动化打包。
    """
    print(">>> 开始自动化构建Lyra项目...")

    # 1. 定位UAT (Unreal Automation Tool) 脚本
    uat_script_path = os.path.join(UE_ENGINE_PATH, "Engine", "Build", "BatchFiles", "RunUAT.bat")
    if not os.path.exists(uat_script_path):
        print(f"错误：在'{uat_script_path}'未找到RunUAT.bat。请检查UE_ENGINE_PATH是否正确。")
        sys.exit(1)

    print(f"UAT脚本位置: {uat_script_path}")
    print(f"Lyra项目文件: {LYRA_PROJECT_PATH}")
    print(f"打包输出目录: {PACKAGE_OUTPUT_PATH}")

    # 2. 构建UAT命令
    # 这是调用UAT进行打包的标准命令格式
    # -clientconfig=Development: 打包开发版本
    # -platform=Win64: 目标平台是Windows 64位
    # -build: 执行构建
    # -cook: 烹饪内容（转换成平台特定格式）
    # -stage: 将所有内容暂存到一个临时目录
    # -package: 将暂存的内容打包
    # -archive: 将打包好的成品归档到指定目录
    # -archivedirectory: 指定归档目录
    command = [
        uat_script_path,
        "BuildCookRun",
        f"-project={LYRA_PROJECT_PATH}",
        "-noP4",
        "-clientconfig=Development",
        "-serverconfig=Development", # 如果需要也可以打包服务器
        "-platform=Win64",
        "-build",
        "-cook",
        "-stage",
        "-package",
        "-archive",
        f"-archivedirectory={PACKAGE_OUTPUT_PATH}"
    ]

    print("\n>>> 即将执行以下命令:")
    # 用空格连接命令列表，方便打印查看
    print(" ".join(command))
    print("\n>>> 构建过程可能需要很长时间，请耐心等待...\n")

    # 3. 执行命令
    try:
        # 使用subprocess.run来执行命令，并实时捕获输出
        # shell=True在Windows上对于.bat文件是必需的
        result = subprocess.run(command, shell=True, check=True, text=True)
        print("\n>>> 构建成功!")
        print(f"打包成品已输出到: {PACKAGE_OUTPUT_PATH}")

    except subprocess.CalledProcessError as e:
        print("\n>>> 构建失败! UAT返回了错误。")
        print(f"返回码: {e.returncode}")
        # 错误输出在e.stderr中，但实时输出时已经打印在控制台
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n>>> 用户手动中断了构建。")
        sys.exit(1)


if __name__ == "__main__":
    main()