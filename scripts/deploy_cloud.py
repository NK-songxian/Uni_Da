# -*- coding: utf-8 -*-
"""
UNIDA uniCloud 一键部署脚本
------------------------------------------------------------------
用 HBuilderX CLI 直接上传云函数 + 公共模块 + 数据库 Schema，
不用在 HBuilderX 里逐个右键。

用法：
    E:/anaco/envs/sam_gpu/python.exe scripts/deploy_cloud.py            # 全量上传（强制覆盖）
    E:/anaco/envs/sam_gpu/python.exe scripts/deploy_cloud.py --check    # 只列出当前资源，不上传
"""
import os
import subprocess
import sys

ROOT = r"H:\UniDA\unida"
CLOUD_DIR = os.path.join(ROOT, "uniCloud-alipay", "cloudfunctions")
COMMON_DIR = os.path.join(CLOUD_DIR, "common")
DB_DIR = os.path.join(ROOT, "uniCloud-alipay", "database")
PROJECT = "unida"
PROVIDER = "alipay"

CLI_CANDIDATES = [
    os.environ.get("HBX_CLI", ""),
    r"H:\HBuilderX\cli.exe",
    r"C:\Program Files\HBuilderX\cli.exe",
    r"D:\HBuilderX\cli.exe",
]


def find_cli():
    for p in CLI_CANDIDATES:
        if p and os.path.isfile(p):
            return p
    return "cli"  # 交给 PATH 查找


def run(args, label):
    print(f"\n== {label} ==")
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.stdout:
        print(p.stdout.rstrip())
    if p.stderr:
        print(p.stderr.rstrip())
    if p.returncode != 0:
        raise SystemExit(f"[失败] {label} 退出码 {p.returncode}")
    return p.stdout


def main():
    cli = find_cli()
    check_only = "--check" in sys.argv

    if check_only:
        run([cli, "cloud", "functions", "--list", "space", "--prj", PROJECT, "--provider", PROVIDER], "服务空间")
        run([cli, "cloud", "functions", "--list", "cloudfunction", "--prj", PROJECT, "--provider", PROVIDER, "--cloud"], "云端云函数")
        run([cli, "cloud", "functions", "--list", "common", "--prj", PROJECT, "--provider", PROVIDER, "--cloud"], "云端公共模块")
        run([cli, "cloud", "functions", "--list", "db", "--prj", PROJECT, "--provider", PROVIDER, "--cloud"], "云端集合")
        return

    # 逐个上传公共模块：跳过空目录（--upload all 遇到空模块会中断，故不用 all）
    common_names = [d for d in sorted(os.listdir(COMMON_DIR))
                    if os.path.isdir(os.path.join(COMMON_DIR, d))
                    and os.listdir(os.path.join(COMMON_DIR, d))]
    for name in common_names:
        run([cli, "cloud", "functions", "--upload", "common", "--prj", PROJECT,
             "--provider", PROVIDER, "--name", name, "--force"], f"上传公共模块 {name}")

    # 逐个上传云函数
    fn_names = [d for d in sorted(os.listdir(CLOUD_DIR))
                if d != "common" and os.path.isdir(os.path.join(CLOUD_DIR, d))
                and os.listdir(os.path.join(CLOUD_DIR, d))]
    for name in fn_names:
        run([cli, "cloud", "functions", "--upload", "cloudfunction", "--prj", PROJECT,
             "--provider", PROVIDER, "--name", name, "--force"], f"上传云函数 {name}")

    schemas = sorted(f for f in os.listdir(DB_DIR) if f.endswith(".schema.json"))
    for name in schemas:
        run([cli, "cloud", "functions", "--upload", "db", "--prj", PROJECT,
             "--provider", PROVIDER, "--name", name, "--force"], f"上传集合 {name}")

    print("\n全部部署完成。用 --check 可核对云端资源。")


if __name__ == "__main__":
    main()
