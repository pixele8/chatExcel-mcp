#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编码缓存管理工具
提供缓存清理、监控、备份等功能
"""

import argparse
import sys
from pathlib import Path
from enhanced_excel_helper import EncodingCache
import json
from datetime import datetime

def format_timestamp(timestamp):
    """格式化时间戳为可读格式"""
    if timestamp:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return 'N/A'

def format_size(size_mb):
    """格式化文件大小"""
    if size_mb < 1:
        return f"{size_mb * 1024:.2f} KB"
    return f"{size_mb:.2f} MB"

def show_cache_stats(cache_dir=".encoding_cache"):
    """显示缓存统计信息"""
    cache = EncodingCache(cache_dir)
    stats = cache.get_cache_stats()
    
    if 'error' in stats:
        print(f"获取统计信息失败: {stats['error']}")
        return
    
    print("\n=== 编码缓存统计信息 ===")
    print(f"缓存条目总数: {stats['total_entries']}")
    print(f"缓存文件大小: {format_size(stats['file_size_mb'])}")
    print(f"过期条目数量: {stats['expired_count']}")
    print(f"最旧条目时间: {format_timestamp(stats['oldest_entry'])}")
    print(f"最新条目时间: {format_timestamp(stats['newest_entry'])}")
    
    # 显示缓存目录信息
    cache_path = Path(cache_dir)
    if cache_path.exists():
        print(f"\n缓存目录: {cache_path.absolute()}")
        cache_file = cache_path / "encoding_cache.json"
        backup_file = cache_path / "encoding_cache_backup.json"
        
        print(f"主缓存文件: {'存在' if cache_file.exists() else '不存在'}")
        print(f"备份文件: {'存在' if backup_file.exists() else '不存在'}")

def cleanup_cache(cache_dir=".encoding_cache"):
    """清理过期缓存"""
    print("开始清理过期缓存...")
    cache = EncodingCache(cache_dir)
    cache._cleanup_expired_cache()
    print("缓存清理完成")

def monitor_cache(cache_dir=".encoding_cache"):
    """监控缓存大小"""
    print("检查缓存大小...")
    cache = EncodingCache(cache_dir)
    cache._monitor_cache_size()

def backup_cache(cache_dir=".encoding_cache"):
    """备份缓存"""
    print("创建缓存备份...")
    cache = EncodingCache(cache_dir)
    if cache.create_backup():
        print("备份创建成功")
    else:
        print("备份创建失败")

def restore_cache(cache_dir=".encoding_cache"):
    """从备份恢复缓存"""
    print("从备份恢复缓存...")
    cache = EncodingCache(cache_dir)
    if cache.restore_from_backup():
        print("缓存恢复成功")
    else:
        print("缓存恢复失败")

def optimize_cache(cache_dir=".encoding_cache"):
    """优化缓存（清理+监控+备份）"""
    print("开始缓存优化...")
    cache = EncodingCache(cache_dir)
    
    # 先备份
    print("1. 创建备份...")
    cache.create_backup()
    
    # 清理过期
    print("2. 清理过期条目...")
    cache._cleanup_expired_cache()
    
    # 监控大小
    print("3. 检查缓存大小...")
    cache._monitor_cache_size()
    
    print("缓存优化完成")

def export_cache_info(cache_dir=".encoding_cache", output_file="cache_report.json"):
    """导出缓存信息到文件"""
    cache = EncodingCache(cache_dir)
    stats = cache.get_cache_stats()
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'cache_directory': str(Path(cache_dir).absolute()),
        'statistics': stats,
        'cache_entries': []
    }
    
    # 添加详细的缓存条目信息
    for key, entry in cache.cache.items():
        report['cache_entries'].append({
            'hash': key,
            'file_path': entry.get('file_path', 'unknown'),
            'encoding': entry.get('encoding', 'unknown'),
            'timestamp': entry.get('timestamp', 0),
            'formatted_time': format_timestamp(entry.get('timestamp', 0))
        })
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"缓存报告已导出到: {output_file}")
    except Exception as e:
        print(f"导出报告失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='编码缓存管理工具')
    parser.add_argument('--cache-dir', default='.encoding_cache', 
                       help='缓存目录路径 (默认: .encoding_cache)')
    parser.add_argument('--max-size', type=int, default=10, help='最大缓存大小(MB)')
    parser.add_argument('--config', default='cache_config.json', help='配置文件路径')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 统计信息
    subparsers.add_parser('stats', help='显示缓存统计信息')
    
    # 清理
    subparsers.add_parser('cleanup', help='清理过期缓存')
    
    # 监控
    subparsers.add_parser('monitor', help='监控缓存大小')
    
    # 备份
    subparsers.add_parser('backup', help='创建缓存备份')
    
    # 恢复
    subparsers.add_parser('restore', help='从备份恢复缓存')
    
    # 优化
    subparsers.add_parser('optimize', help='优化缓存（清理+监控+备份）')
    
    # 导出
    export_parser = subparsers.add_parser('export', help='导出缓存信息')
    export_parser.add_argument('--output', default='cache_report.json',
                              help='输出文件名 (默认: cache_report.json)')
    
    args = parser.parse_args()
    
    # 创建缓存管理器实例（优先使用配置文件）
    cache_manager = EncodingCache(args.cache_dir, args.max_size, args.config)
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'stats':
            show_cache_stats(args.cache_dir)
        elif args.command == 'cleanup':
            cleanup_cache(args.cache_dir)
        elif args.command == 'monitor':
            monitor_cache(args.cache_dir)
        elif args.command == 'backup':
            backup_cache(args.cache_dir)
        elif args.command == 'restore':
            restore_cache(args.cache_dir)
        elif args.command == 'optimize':
            optimize_cache(args.cache_dir)
        elif args.command == 'export':
            export_cache_info(args.cache_dir, args.output)
    except Exception as e:
        print(f"执行命令失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()