# 编码缓存优化系统

## 概述

本项目实现了一个智能的编码缓存管理系统，用于优化Excel文件编码检测的性能。系统支持自动清理、大小监控、备份恢复等功能，确保缓存系统的高效运行。

## 功能特性

### 🚀 核心功能
- **智能编码检测缓存**：自动缓存文件编码检测结果
- **自动过期清理**：定期清理过期的缓存条目
- **大小监控**：实时监控缓存文件大小，防止无限增长
- **自动备份**：定期创建缓存备份，保障数据安全
- **配置驱动**：通过JSON配置文件灵活控制所有参数

### 📊 性能优化
- **减少重复检测**：避免对同一文件重复进行编码检测
- **智能缓存策略**：基于文件哈希和时间戳的缓存机制
- **内存友好**：控制缓存大小，避免内存溢出
- **异步清理**：后台自动执行维护任务

## 配置说明

### 配置文件：`cache_config.json`

```json
{
  "cache_settings": {
    "max_cache_size_mb": 10,           // 最大缓存大小(MB)
    "cache_expiry_days": 7,            // 缓存过期天数
    "auto_cleanup_interval": 10,       // 自动清理间隔(次数)
    "enable_auto_backup": true         // 启用自动备份
  },
  "monitoring": {
    "enable_size_monitoring": true,    // 启用大小监控
    "size_warning_threshold_mb": 8,    // 大小警告阈值(MB)
    "enable_performance_logging": false, // 启用性能日志
    "log_level": "INFO"                // 日志级别
  },
  "maintenance": {
    "auto_reduce_cache_percentage": 50, // 自动减少缓存百分比
    "enable_startup_cleanup": true,    // 启用启动时清理
    "enable_periodic_optimization": true, // 启用定期优化
    "optimization_frequency": "weekly" // 优化频率
  },
  "paths": {
    "cache_directory": ".encoding_cache", // 缓存目录
    "backup_directory": ".encoding_cache", // 备份目录
    "log_file": "cache_maintenance.log"    // 日志文件
  }
}
```

### 配置参数详解

#### 缓存设置 (cache_settings)
- `max_cache_size_mb`: 缓存文件的最大大小限制
- `cache_expiry_days`: 缓存条目的有效期（天数）
- `auto_cleanup_interval`: 每N次写入操作后执行一次自动清理
- `enable_auto_backup`: 是否启用自动备份功能

#### 监控设置 (monitoring)
- `enable_size_monitoring`: 是否启用缓存大小监控
- `size_warning_threshold_mb`: 发出警告的大小阈值
- `enable_performance_logging`: 是否启用详细的性能日志
- `log_level`: 日志记录级别

#### 维护设置 (maintenance)
- `auto_reduce_cache_percentage`: 当缓存超限时，删除最旧条目的百分比
- `enable_startup_cleanup`: 是否在启动时执行清理
- `enable_periodic_optimization`: 是否启用定期优化

## 使用方法

### 1. 命令行工具

#### 基本用法
```bash
# 查看缓存统计信息
python cache_manager.py stats

# 清理过期缓存
python cache_manager.py cleanup

# 监控缓存大小
python cache_manager.py monitor

# 创建备份
python cache_manager.py backup

# 从备份恢复
python cache_manager.py restore

# 执行完整优化（清理+监控+备份）
python cache_manager.py optimize

# 导出缓存信息
python cache_manager.py export --export-file cache_data.json
```

#### 使用自定义配置
```bash
# 使用指定的配置文件
python cache_manager.py --config my_config.json stats

# 使用自定义缓存目录
python cache_manager.py --cache-dir /path/to/cache stats
```

### 2. 自动化维护

#### 使用维护脚本
```bash
# 手动执行维护
./scripts/cache_maintenance.sh

# 查看维护日志
tail -f cache_maintenance.log
```

#### 设置定时任务
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天凌晨2点执行维护）
0 2 * * * /path/to/chatExcel-mcp-server/scripts/cache_maintenance.sh

# 每周日凌晨3点执行深度优化
0 3 * * 0 /path/to/chatExcel-mcp-server/scripts/cache_maintenance.sh
```

### 3. 程序集成

#### 在Python代码中使用
```python
from enhanced_excel_helper import EncodingCache

# 使用默认配置
cache = EncodingCache()

# 使用自定义配置文件
cache = EncodingCache(config_file="my_config.json")

# 获取文件编码（自动缓存）
encoding = cache.get("/path/to/file.xlsx")
if not encoding:
    # 检测并缓存编码
    detected_encoding = detect_file_encoding("/path/to/file.xlsx")
    cache.set("/path/to/file.xlsx", detected_encoding)

# 获取缓存统计
stats = cache.get_cache_stats()
print(f"缓存条目数: {stats['total_entries']}")
print(f"缓存文件大小: {stats['cache_size_mb']:.2f} MB")
```

## 监控和维护

### 性能监控

1. **缓存命中率监控**
   ```bash
   python cache_manager.py stats
   ```

2. **大小监控**
   ```bash
   python cache_manager.py monitor
   ```

3. **日志监控**
   ```bash
   tail -f cache_maintenance.log
   ```

### 故障排除

#### 常见问题

1. **缓存文件过大**
   - 检查配置中的 `max_cache_size_mb` 设置
   - 执行手动清理：`python cache_manager.py cleanup`
   - 调整 `auto_cleanup_interval` 参数

2. **性能下降**
   - 检查缓存命中率
   - 考虑增加 `cache_expiry_days`
   - 启用性能日志进行详细分析

3. **配置文件错误**
   - 检查JSON格式是否正确
   - 验证所有必需字段是否存在
   - 查看启动日志中的错误信息

#### 恢复操作

1. **从备份恢复**
   ```bash
   python cache_manager.py restore
   ```

2. **重置缓存**
   ```bash
   rm -rf .encoding_cache
   # 缓存将在下次使用时自动重建
   ```

3. **重置配置**
   ```bash
   # 删除配置文件，将使用默认配置
   rm cache_config.json
   ```

## 最佳实践

### 生产环境建议

1. **配置优化**
   - 根据文件处理量调整 `max_cache_size_mb`
   - 设置合适的 `cache_expiry_days`（建议7-30天）
   - 启用 `enable_auto_backup`

2. **监控设置**
   - 在生产环境中启用 `enable_size_monitoring`
   - 设置合理的 `size_warning_threshold_mb`
   - 考虑启用 `enable_performance_logging` 进行性能分析

3. **维护计划**
   - 设置每日自动维护任务
   - 定期检查缓存统计信息
   - 监控日志文件大小

### 开发环境建议

1. **调试配置**
   - 启用 `enable_performance_logging`
   - 设置较小的 `auto_cleanup_interval` 进行测试
   - 使用较短的 `cache_expiry_days`

2. **测试验证**
   - 定期执行 `python cache_manager.py stats`
   - 测试备份和恢复功能
   - 验证自动清理机制

## 版本历史

- **v1.0.0**: 基础缓存功能
- **v1.1.0**: 添加自动清理和监控
- **v1.2.0**: 增加备份恢复功能
- **v1.3.0**: 实现配置文件支持
- **v1.4.0**: 完善命令行工具和自动化脚本

## 技术支持

如有问题或建议，请：
1. 检查本文档的故障排除部分
2. 查看日志文件获取详细错误信息
3. 提交Issue或联系技术支持团队

---

**注意**: 本缓存系统设计为向后兼容，即使没有配置文件也能正常工作，但建议使用配置文件以获得最佳性能和灵活性。