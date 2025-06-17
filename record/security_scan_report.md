
# 安全扫描报告

生成时间: 2025-06-14T13:26:20.677184

## 概览
- 依赖漏洞: 0 个
- 代码漏洞: 1138 个
- 配置问题: 2 个
- 文件权限问题: 9 个

## 依赖漏洞详情

## 代码安全问题

### server.py:42
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### server.py:42
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### config.py:11
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### config.py:11
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### enhanced_run_excel_code.py:20
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### enhanced_run_excel_code.py:20
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### enhanced_run_excel_code.py:261
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### generate_mcp_config.py:44
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### server_original.py:33
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### server_original.py:33
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_original.py:748
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_original.py:860
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_backup_param_fix_20250607_121729.py:33
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### server_backup_param_fix_20250607_121729.py:33
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_backup_param_fix_20250607_121729.py:834
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_backup_param_fix_20250607_121729.py:981
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### debug_pandas_issue.py:122
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### debug_pandas_issue.py:131
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_backup_20250607_121037.py:33
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### server_backup_20250607_121037.py:33
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_backup_20250607_121037.py:748
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### server_backup_20250607_121037.py:860
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test_enhanced_features.py:64
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### test_enhanced_features.py:63
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test_enhanced_features.py:62
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### test_formulas_integration.py:49
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: EXEC(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### pandas_fix_patch.py:236
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test/test_numpy_mcp_integration.py:168
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test/test_numpy_mcp_integration.py:316
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test/test_numpy_mcp_integration.py:402
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test/debug_pandas_issue.py:122
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test/debug_pandas_issue.py:131
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### test/test_pandas_import.py:97
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### security/secure_code_executor.py:307
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### scripts/security_enhancer.py:401
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### scripts/security_enhancer.py:401
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### scripts/security_enhancer.py:402
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### scripts/security_enhancer.py:404
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### venv/lib/python3.11/site-packages/six.py:740
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/typing_extensions.py:1396
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:3961
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:3966
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:4013
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:4025
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:4030
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:4058
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/typing_extensions.py:1396
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/packaging/_parser.py:332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/packaging/licenses/__init__.py:100
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/mypyc/test/test_run.py:366
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/mypyc/test/test_run.py:110
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/mypyc/test/test_external.py:43
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/mypyc/test-data/fixtures/ir.py:350
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pygments/lexers/_julia_builtins.py:150
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pygments/lexers/_julia_builtins.py:361
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pygments/lexers/__init__.py:154
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pygments/lexers/installers.py:66
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: Exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pygments/lexers/foxpro.py:70
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: EVAL(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pygments/lexers/special.py:115
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pygments/formatters/__init__.py:91
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pygments/formatters/__init__.py:103
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:1562
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:1982
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:3254
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:2009
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:2012
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:2013
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:2014
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:2015
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pycparser/ply/yacc.py:2016
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pycparser/ply/lex.py:215
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pycparser/ply/lex.py:1039
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pycparser/ply/cpp.py:600
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pyparsing/results.py:62
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/jinja2/debug.py:145
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/jinja2/lexer.py:663
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/jinja2/environment.py:1228
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/jinja2/nativetypes.py:40
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/jinja2/nodes.py:581
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/jinja2/bccache.py:73
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/seaborn/distributions.py:471
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/seaborn/_stats/counting.py:165
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/seaborn/_stats/counting.py:170
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/seaborn/_stats/density.py:211
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/cffi/setuptools_ext.py:25
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/cffi/recompiler.py:78
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/starlette/datastructures.py:174
- **问题类型**: hardcoded_password
- **严重程度**: high
- **描述**: password="********"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密码


### venv/lib/python3.11/site-packages/serializable/__init__.py:957
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/serializable/__init__.py:958
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/serializable/__init__.py:990
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/serializable/__init__.py:991
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/misc/psLib.py:152
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/misc/psLib.py:159
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/misc/symfont.py:241
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/misc/psOperators.py:270
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/misc/psOperators.py:341
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/misc/psOperators.py:343
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/misc/psOperators.py:348
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/misc/xmlReader.py:106
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/misc/xmlReader.py:122
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/feaLib/builder.py:498
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_s_b_i_x.py:109
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G_M_A_P_.py:56
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G_M_A_P_.py:148
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F_F_T_M_.py:51
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_O_R_G_.py:119
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_O_R_G_.py:165
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_k_e_r_n.py:98
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_k_e_r_n.py:104
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_k_e_r_n.py:236
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_k_e_r_n.py:237
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_k_e_r_n.py:240
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_k_e_r_n.py:254
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/TupleVariation.py:121
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/TupleVariation.py:122
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/TupleVariation.py:123
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/TupleVariation.py:126
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/TupleVariation.py:127
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_f.py:316
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_f.py:415
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_f.py:416
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_f.py:417
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_f.py:607
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_f.py:772
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_h_d_m_x.py:123
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S_I_N_G_.py:66
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S_I_N_G_.py:99
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/T_S_I__5.py:60
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:350
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:352
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:354
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:355
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:358
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:360
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:365
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:546
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:548
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:550
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:609
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:614
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:616
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:618
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:747
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:752
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:758
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:869
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1098
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1099
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1100
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1154
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1155
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1729
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otTables.py:1912
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:80
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:623
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1217
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1232
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1234
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1534
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1554
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1564
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1595
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1642
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1706
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1805
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otConverters.py:1819
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_p_o_s_t.py:264
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:238
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:244
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:246
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:247
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:419
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:429
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:772
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:783
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1055
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1066
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1122
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1133
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1290
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1291
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1292
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1293
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1294
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1305
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1456
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_m_a_p.py:1457
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/C_P_A_L_.py:268
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/C_P_A_L_.py:269
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/C_P_A_L_.py:276
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_l.py:81
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S__i_l_l.py:91
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:174
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:178
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:186
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:227
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:331
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:333
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:334
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:377
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:379
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:380
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_D_T_.py:475
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F__e_a_t.py:130
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F__e_a_t.py:134
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F__e_a_t.py:135
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F__e_a_t.py:136
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F__e_a_t.py:145
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/F__e_a_t.py:145
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/C_O_L_R_.py:108
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/C_O_L_R_.py:165
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G__l_o_c.py:76
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_l_t_a_g.py:71
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/D_S_I_G_.py:114
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/D_S_I_G_.py:115
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/D_S_I_G_.py:116
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/D_S_I_G_.py:155
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/D_S_I_G_.py:156
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/D_S_I_G_.py:157
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:276
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:795
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:795
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:796
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:797
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:799
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:1917
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:1918
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:1920
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:1921
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_l_y_f.py:1935
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_v_t.py:41
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_c_v_t.py:42
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:206
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:220
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:221
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:222
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:223
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:224
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:245
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:246
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/V_D_M_X_.py:247
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_a_v_a_r.py:124
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_a_v_a_r.py:125
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_m_a_x_p.py:147
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_n_a_m_e.py:621
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_n_a_m_e.py:622
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_n_a_m_e.py:623
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_n_a_m_e.py:624
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_n_a_m_e.py:627
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/M_E_T_A_.py:211
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/M_E_T_A_.py:243
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/M_E_T_A_.py:286
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/M_E_T_A_.py:328
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_h_h_e_a.py:147
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_v_h_e_a.py:130
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/S_V_G_.py:186
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/L_T_S_H_.py:58
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixStrike.py:140
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixStrike.py:143
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixStrike.py:147
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixStrike.py:149
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixStrike.py:155
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixStrike.py:159
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:254
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:258
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:296
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:342
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:364
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:432
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:433
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:434
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/E_B_L_C_.py:569
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_h_e_a_d.py:129
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_h_m_t_x.py:149
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_h_m_t_x.py:150
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G__l_a_t.py:202
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G__l_a_t.py:203
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G__l_a_t.py:215
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G__l_a_t.py:216
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/O_S_2f_2.py:42
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/O_S_2f_2.py:253
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/O_S_2f_2.py:255
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/BitmapGlyphMetrics.py:50
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otBase.py:952
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otBase.py:990
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otBase.py:1094
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/otBase.py:1137
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/sbixGlyph.py:141
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_f_v_a_r.py:175
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_f_v_a_r.py:251
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_f_v_a_r.py:252
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_f_v_a_r.py:254
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_v_a_r.py:257
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_v_a_r.py:259
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_t_r_a_k.py:118
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_t_r_a_k.py:120
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_t_r_a_k.py:292
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_t_r_a_k.py:300
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_a_s_p.py:61
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/_g_a_s_p.py:61
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/ttLib/tables/G_P_K_G_.py:133
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/cffLib/__init__.py:1100
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/cffLib/__init__.py:1267
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/cffLib/__init__.py:1718
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/cffLib/__init__.py:1883
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/cffLib/__init__.py:2026
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/fontTools/cffLib/__init__.py:2498
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/fontTools/t1Lib/__init__.py:158
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/fontTools/t1Lib/__init__.py:168
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/click/_termui_impl.py:533
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/click/_termui_impl.py:697
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/click/_termui_impl.py:711
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/websockets/cli.py:167
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/mcp/shared/_httpx_utils.py:60
- **问题类型**: hardcoded_password
- **严重程度**: high
- **描述**: password="pass"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密码


### venv/lib/python3.11/site-packages/pytz/__init__.py:283
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pytz/__init__.py:486
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pytz/__init__.py:488
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/regex/test_regex.py:3775
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/distutils/misc_util.py:157
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/distutils/misc_util.py:163
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/distutils/misc_util.py:847
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/distutils/mingw32ccompiler.py:340
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/numpy/distutils/_shell_utils.py:33
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/numpy/distutils/_shell_utils.py:73
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/numpy/distutils/tests/test_ccompiler_opt.py:805
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/numpy/ma/timer_comparison.py:441
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_old_ma.py:555
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_core.py:636
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_core.py:651
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_core.py:660
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_core.py:670
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_core.py:680
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_core.py:5452
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/ma/tests/test_mrecords.py:289
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/_internal.py:204
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/records.py:705
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/arrayprint.py:1545
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_scalarmath.py:613
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_scalarmath.py:639
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_arrayprint.py:332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_arrayprint.py:333
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_deprecations.py:644
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:166
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:167
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:169
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:410
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:411
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:417
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:418
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:425
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_records.py:449
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:241
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:507
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:637
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:698
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:718
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:738
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:764
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:801
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:840
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:892
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_simd.py:1098
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_umath.py:499
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_umath.py:563
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:846
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:848
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:850
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:853
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:860
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:864
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_datetime.py:868
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test__exceptions.py:18
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test__exceptions.py:83
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_custom_dtypes.py:304
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_ufunc.py:196
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_ufunc.py:201
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_ufunc.py:208
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_ufunc.py:218
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_ufunc.py:495
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_dtype.py:1057
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_dtype.py:1354
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_dtype.py:1416
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_dtype.py:1427
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_umath_accuracy.py:68
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_umath_accuracy.py:69
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_stringdtype.py:388
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_overrides.py:227
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:1533
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:3881
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:173
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:1685
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:1839
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:1846
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:1855
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:1866
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4363
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4365
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4386
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4399
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4417
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4426
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:4480
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_multiarray.py:8231
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:40
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:351
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:477
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:821
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1059
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1072
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1265
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1267
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1900
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1912
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1924
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1950
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:1959
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:2205
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:2429
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/_core/tests/test_regression.py:2561
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/tests/test_reloading.py:45
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/tests/test_public_api.py:420
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:1332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2299
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2301
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2331
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2353
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2359
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2365
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2372
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2563
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2593
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2671
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2680
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2948
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:2998
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:3019
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:3050
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/crackfortran.py:3508
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/diagnose.py:9
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/numpy/f2py/capi_maps.py:157
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/capi_maps.py:295
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/capi_maps.py:451
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/auxfuncs.py:614
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/auxfuncs.py:622
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/auxfuncs.py:626
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/tests/test_crackfortran.py:256
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: Eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/tests/test_crackfortran.py:365
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/tests/test_crackfortran.py:375
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/tests/test_crackfortran.py:394
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/f2py/tests/test_f2py2e.py:847
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/numpy/f2py/tests/test_f2py2e.py:855
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/numpy/testing/_private/utils.py:1257
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/numpy/testing/_private/utils.py:1543
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/numpy/lib/format.py:521
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/format.py:546
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/format.py:641
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/format.py:646
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/format.py:781
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/format.py:900
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/format.py:820
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/lib/_npyio_impl.py:142
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_npyio_impl.py:353
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_npyio_impl.py:489
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/lib/_npyio_impl.py:491
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:576
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:610
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:612
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:614
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:617
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:622
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/lib/_utils_impl.py:640
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/random/tests/test_generator_mt19937.py:2769
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_generator_mt19937.py:2775
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_generator_mt19937.py:2791
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_randomstate.py:262
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_direct.py:290
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_direct.py:298
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_direct.py:308
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_direct.py:314
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_direct.py:543
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_smoke.py:436
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/random/tests/test_smoke.py:442
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/matrixlib/tests/test_masked_matrix.py:81
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:246
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:248
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:304
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:307
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:791
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:797
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:857
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:859
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:1088
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/hermite_e.py:1357
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:81
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:85
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:87
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:122
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:124
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:132
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:139
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:140
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:141
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:239
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:360
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:368
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:425
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:428
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:432
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:435
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:439
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:468
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:470
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_hermite_e.py:516
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/numpy/polynomial/tests/test_polynomial.py:54
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/PIL/GifImagePlugin.py:726
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/GifImagePlugin.py:748
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:236
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:278
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:284
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:335
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:342
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:350
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:350
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageMath.py:368
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/PIL/ImageShow.py:120
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/PIL/ImageShow.py:177
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/PIL/ImageGrab.py:49
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/PIL/ImageGrab.py:98
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: subprocess.call(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/PIL/Image.py:3634
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/safety/util.py:873
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### venv/lib/python3.11/site-packages/safety/scan/util.py:48
- **问题类型**: hardcoded_api_key
- **严重程度**: high
- **描述**: api_key = "api_key"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储API密钥


### venv/lib/python3.11/site-packages/_plotly_utils/basevalidators.py:2128
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/html5lib/_inputstream.py:32
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/html5lib/_utils.py:33
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/html5lib/_utils.py:36
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/anyio/to_process.py:86
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/anyio/to_process.py:210
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/anyio/to_interpreter.py:111
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/anyio/to_interpreter.py:116
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py:2561
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_internal/utils/misc.py:478
- **问题类型**: hardcoded_password
- **严重程度**: high
- **描述**: password = ":****"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密码


### venv/lib/python3.11/site-packages/pip/_internal/utils/setuptools_build.py:10
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_internal/utils/setuptools_build.py:44
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:1300
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:4279
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:4284
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:4331
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:4343
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:4348
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:4376
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/typing_extensions.py:1300
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/packaging/_parser.py:332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/packaging/licenses/__init__.py:100
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/pygments/lexers/__init__.py:154
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/pygments/formatters/__init__.py:91
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/pygments/formatters/__init__.py:103
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/distlib/scripts.py:163
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/rich/markup.py:190
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pip/_vendor/urllib3/packages/six.py:787
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec (
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/pkg_resources/__init__.py:1714
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip/_vendor/pkg_resources/__init__.py:1725
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/httpx/_urls.py:336
- **问题类型**: hardcoded_password
- **严重程度**: high
- **描述**: password="a secret"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密码


### venv/lib/python3.11/site-packages/schedula/ext/dispatcher/documenter.py:254
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/schedula/ext/dispatcher/documenter.py:88
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/schedula/utils/drw/__init__.py:679
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/schedula/utils/form/cli.py:143
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/schedula/utils/form/cli.py:200
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/schedula/utils/form/server/credits.py:729
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/schedula/utils/asy/__init__.py:223
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/safety_schemas/models/config.py:461
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### venv/lib/python3.11/site-packages/safety_schemas/models/base.py:89
- **问题类型**: hardcoded_api_key
- **严重程度**: high
- **描述**: API_KEY = "api_key"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储API密钥


### venv/lib/python3.11/site-packages/safety_schemas/report/schemas/v3_0/main.py:143
- **问题类型**: hardcoded_api_key
- **严重程度**: high
- **描述**: api_key = "api_key"
- **修复建议**: 使用环境变量或安全的密钥管理系统存储API密钥


### venv/lib/python3.11/site-packages/cyclonedx/model/crypto.py:703
- **问题类型**: hardcoded_password
- **严重程度**: high
- **描述**: PASSWORD = 'password'
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密码


### venv/lib/python3.11/site-packages/cyclonedx/model/crypto.py:709
- **问题类型**: hardcoded_secret
- **严重程度**: high
- **描述**: SECRET = 'shared-secret'
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密钥


### venv/lib/python3.11/site-packages/mypy/evalexpr.py:30
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/mypy/evalexpr.py:32
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/mypy/modulefinder.py:734
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/mypy/dmypy/client.py:623
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/RestrictedPython/compile.py:96
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/RestrictedPython/compile.py:80
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/RestrictedPython/Eval.py:65
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/RestrictedPython/Eval.py:93
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/RestrictedPython/Eval.py:110
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/RestrictedPython/Eval.py:113
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/rich/markup.py:190
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/blib2to3/pgen2/pgen.py:100
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/blib2to3/pgen2/literals.py:4
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/blib2to3/pgen2/grammar.py:124
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/blib2to3/pgen2/grammar.py:129
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/blib2to3/pgen2/conv.py:186
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/blib2to3/pgen2/conv.py:212
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pluggy/_hooks.py:512
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pluggy/_hooks.py:534
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pluggy/_hooks.py:573
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pluggy/_hooks.py:580
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pluggy/_manager.py:111
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pluggy/_manager.py:120
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pluggy/_manager.py:464
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:347
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:485
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:802
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:827
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:830
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:834
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/rcsetup.py:1104
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/sphinxext/plot_directive.py:543
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/sphinxext/plot_directive.py:546
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/sphinxext/plot_directive.py:552
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/sphinxext/plot_directive.py:554
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/backend_qt.py:460
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/backend_qt.py:641
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/qt_compat.py:157
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/qt_compat.py:159
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/qt_editor/_formlayout.py:355
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/backends/qt_editor/_formlayout.py:576
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/qt_editor/_formlayout.py:582
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/backends/qt_editor/_formlayout.py:592
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:164
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:117
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:133
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:164
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:180
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:217
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:242
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:255
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:263
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:272
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:286
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:293
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:297
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:304
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:310
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_pickle.py:317
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_patches.py:475
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/tests/test_rcparams.py:299
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/matplotlib/tests/test_transforms.py:868
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/tests/test_transforms.py:869
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/tests/test_transforms.py:873
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/tests/test_transforms.py:875
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/matplotlib/tests/test_cbook.py:227
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_cbook.py:323
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/matplotlib/tests/test_figure.py:1691
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/loguru/_logger.py:1508
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/loguru/_recattrs.py:84
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/loguru/_recattrs.py:86
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/setuptools/launch.py:32
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/build_meta.py:317
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/wheel.py:190
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/wheel.py:211
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/typing_extensions.py:1215
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/typing_extensions.py:1215
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/_vendor/packaging/_parser.py:332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/packaging/licenses/__init__.py:100
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/jaraco/functools/__init__.py:522
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/wheel/vendored/packaging/_parser.py:334
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/more_itertools/recipes.py:992
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/_vendor/more_itertools/recipes.py:999
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/config/expand.py:72
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/tests/test_extern.py:15
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/setuptools/tests/test_egg_info.py:277
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/tests/test_editable_install.py:449
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/tests/namespaces.py:34
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/setuptools/tests/config/test_pyprojecttoml.py:98
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/_distutils/core.py:228
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/_distutils/core.py:268
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/setuptools/_distutils/compilers/C/base.py:1120
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pkg_resources/__init__.py:1738
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pkg_resources/__init__.py:1749
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pip_api/_vendor/pyparsing.py:523
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pydantic/types.py:1695
- **问题类型**: hardcoded_password
- **严重程度**: high
- **描述**: password='password1'
- **修复建议**: 使用环境变量或安全的密钥管理系统存储密码


### venv/lib/python3.11/site-packages/pydantic/v1/utils.py:195
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pydantic/v1/parse.py:42
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pydantic/_internal/_typing_extra.py:451
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pydantic/_internal/_typing_extra.py:484
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pydantic/_internal/_typing_extra.py:451
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pydantic/deprecated/parse.py:54
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/typing_inspection/typing_objects.py:100
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/typing_inspection/typing_objects.py:132
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/black/cache.py:79
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/psutil/__init__.py:1901
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval (
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/test_connections.py:361
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/test_connections.py:363
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/test_connections.py:366
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/test_connections.py:368
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/test_misc.py:268
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/psutil/tests/test_misc.py:305
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/psutil/tests/test_misc.py:315
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/psutil/tests/test_misc.py:326
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/psutil/tests/test_misc.py:334
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/psutil/tests/__init__.py:794
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/__init__.py:798
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/psutil/tests/__init__.py:1359
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/psutil/tests/__init__.py:1361
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/scipy/odr/tests/test_odr.py:576
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/odr/tests/test_odr.py:585
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/odr/tests/test_odr.py:589
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/odr/tests/test_odr.py:598
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/odr/tests/test_odr.py:607
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/optimize/_optimize.py:303
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_chandrupatla.py:154
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_chandrupatla.py:159
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_chandrupatla.py:428
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_chandrupatla.py:465
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_nonlin.py:1590
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/optimize/_bracket.py:245
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_bracket.py:263
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_bracket.py:655
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/_bracket.py:671
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/tests/test__differential_evolution.py:260
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/optimize/tests/test_constraints.py:183
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/integrate/_tanhsinh.py:397
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/integrate/_tanhsinh.py:412
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/integrate/tests/test__quad_vec.py:143
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/integrate/_ivp/tests/test_ivp.py:678
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/datasets/_fetchers.py:74
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/_lib/decorator.py:166
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/_bunch.py:160
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/_elementwise_iterative_method.py:227
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/_elementwise_iterative_method.py:250
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/array_api_compat/dask/array/linalg.py:25
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/array_api_compat/dask/array/fft.py:6
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/array_api_compat/cupy/linalg.py:6
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/array_api_compat/cupy/fft.py:6
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/array_api_compat/torch/__init__.py:12
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/_lib/tests/test_bunch.py:59
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/problem.py:80
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/problem.py:560
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/problem.py:886
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/problem.py:947
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/problem.py:1192
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/main.py:650
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/main.py:697
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/main.py:840
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/main.py:1422
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/_lib/cobyqa/main.py:1446
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/special/_precompute/wright_bessel.py:183
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/special/_precompute/wright_bessel.py:203
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/special/tests/test_orthogonal.py:281
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/differentiate/_differentiate.py:439
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/differentiate/_differentiate.py:485
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_bsplines.py:122
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_bsplines.py:130
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_bsplines.py:860
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_bsplines.py:1320
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpnd.py:172
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpnd.py:399
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_polyint.py:788
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_rbfinterp.py:418
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:837
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:1335
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2218
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2224
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2244
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2264
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2468
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2504
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/interpolate/tests/test_interpolate.py:2544
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/sparse/linalg/tests/test_interface.py:397
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/sparse/tests/test_base.py:2216
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/sparse/csgraph/tests/test_graph_laplacian.py:44
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/sparse/csgraph/tests/test_graph_laplacian.py:300
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/sparse/csgraph/tests/test_graph_laplacian.py:302
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_kdtree.py:854
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_kdtree.py:868
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:444
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:451
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:558
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:568
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:753
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:760
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:1391
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:1401
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/tests/test_distance.py:2134
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/spatial/transform/tests/test_rotation.py:1786
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:326
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:377
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:502
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:545
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:561
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:562
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:576
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:621
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:637
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/_spline_filters.py:638
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_signaltools.py:1440
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_signaltools.py:1458
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:143
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:145
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:148
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:167
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:169
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:171
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:174
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/signal/tests/test_bsplines.py:193
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/stats/_distn_infrastructure.py:359
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/stats/_distn_infrastructure.py:735
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/scipy/stats/_continuous_distns.py:3450
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/stats/_continuous_distns.py:3460
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_continuous.py:85
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_continuous.py:1728
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_continuous.py:900
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_multivariate.py:3388
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_axis_nan_policy.py:726
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/common_tests.py:303
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/common_tests.py:316
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/common_tests.py:326
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_distributions.py:6835
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/scipy/stats/tests/test_sampling.py:258
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/coverage/templite.py:74
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/coverage/parser.py:668
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/coverage/execfile.py:211
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4823
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4839
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4843
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4846
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4897
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4908
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4925
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/frame.py:4949
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/ops.py:431
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/eval.py:170
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/eval.py:294
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/scope.py:199
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/expr.py:480
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/expr.py:515
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/expr.py:519
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/expr.py:527
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/expr.py:574
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/core/computation/expr.py:582
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/io/pickle.py:202
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/test_downstream.py:128
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/test_downstream.py:182
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### venv/lib/python3.11/site-packages/pandas/tests/test_downstream.py:185
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### venv/lib/python3.11/site-packages/pandas/tests/extension/test_arrow.py:1551
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/extension/test_arrow.py:1554
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/extension/test_arrow.py:2893
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/io/test_pickle.py:171
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/io/test_pickle.py:637
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.load(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/io/xml/test_xml.py:1277
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/io/xml/test_to_xml.py:1105
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/copy_view/test_methods.py:2002
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/copy_view/test_methods.py:2006
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/copy_view/test_methods.py:2021
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/copy_view/test_astype.py:139
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:60
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:66
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:72
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:79
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:90
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:117
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:120
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:168
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:169
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:179
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:187
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:601
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:604
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:610
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:852
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:867
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:871
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1164
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1169
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1179
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1228
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1233
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1238
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1243
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1248
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1253
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1258
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1263
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1268
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1293
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1305
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1335
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1338
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1341
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1350
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1363
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/test_query_eval.py:1374
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/methods/test_sample.py:176
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/frame/methods/test_sample.py:177
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_compat.py:31
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:146
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:154
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:167
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:181
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:189
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:198
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:226
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:241
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:252
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:265
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:274
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:279
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:299
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:306
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:326
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:335
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:347
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:362
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:375
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:388
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:392
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:399
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:402
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:408
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:417
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:421
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:433
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:437
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:444
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:447
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:453
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:464
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:468
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:476
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:482
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:490
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:493
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:502
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:508
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:516
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:519
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:537
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:555
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:564
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:566
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:567
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:568
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:569
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:570
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:574
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:578
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:579
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:580
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:581
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:582
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:589
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:614
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:621
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:627
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:649
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:654
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:659
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:664
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:670
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:675
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:680
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:688
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:694
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:731
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:732
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:733
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:738
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:739
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:759
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:769
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:791
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:814
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:816
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:829
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:837
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:865
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:867
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:887
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:889
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:928
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:930
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:958
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:960
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:962
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:963
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1011
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1013
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1026
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1030
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1035
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1048
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1067
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1069
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1092
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1095
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1099
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1103
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1115
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1118
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1119
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1131
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1134
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1135
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1143
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1146
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1151
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1157
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1161
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1178
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1188
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1196
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1205
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1213
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1222
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1232
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1241
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1254
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1264
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1267
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1274
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1282
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1295
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1309
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1320
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1346
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1356
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1372
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1392
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1412
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1442
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1451
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1455
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1463
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1469
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1473
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1481
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1492
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1501
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1508
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1519
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1522
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1525
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1528
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1531
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1534
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1537
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1540
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1543
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1546
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1551
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1553
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1555
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1557
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1560
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1562
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1568
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1587
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1595
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1609
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1612
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1616
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1618
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1629
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1646
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1658
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1675
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1700
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1712
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1719
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1729
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1735
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1743
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1752
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1759
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1766
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1802
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1827
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1834
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1843
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1846
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1854
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1856
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1863
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1869
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1874
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1896
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1908
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1920
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:1984
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/computation/test_eval.py:2001
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/arrays/string_/test_string_arrow.py:253
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/arrays/string_/test_string_arrow.py:256
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/generic/test_finalize.py:449
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/test_na_scalar.py:298
- **问题类型**: pickle_load
- **严重程度**: medium
- **描述**: pickle.loads(
- **修复建议**: 避免反序列化不可信数据，考虑使用JSON或其他安全格式


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:652
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:660
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:669
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:677
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_formats.py:110
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_formats.py:116
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_formats.py:126
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/scalar/timestamp/test_formats.py:163
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/test_old_base.py:239
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/ranges/test_range.py:63
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/ranges/test_range.py:71
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/ranges/test_range.py:398
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/base_class/test_formats.py:16
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/multi/test_formats.py:64
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/categorical/test_category.py:203
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/tests/indexes/numeric/test_numeric.py:43
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/errors/__init__.py:567
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pandas/errors/__init__.py:585
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/ruamel/yaml/util.py:196
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### venv/lib/python3.11/site-packages/_pytest/skipping.py:90
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/skipping.py:117
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/capture.py:1048
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/_pytest/capture.py:1076
- **问题类型**: shell_injection
- **严重程度**: high
- **描述**: os.system(
- **修复建议**: 使用subprocess的列表参数形式，避免shell=True


### venv/lib/python3.11/site-packages/_pytest/pytester.py:295
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/mark/__init__.py:65
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/mark/__init__.py:66
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/mark/expression.py:283
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/mark/expression.py:332
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/_code/code.py:163
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/_code/code.py:172
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/_code/code.py:286
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/_pytest/_code/code.py:286
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:184
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/_pytest/_py/path.py:1153
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/_pytest/_py/path.py:1159
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/formulas/functions/__init__.py:449
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/formulas/functions/__init__.py:472
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/formulas/functions/__init__.py:475
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/formulas/tokens/operand.py:99
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### venv/lib/python3.11/site-packages/pyflakes/test/test_imports.py:680
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: Exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pyflakes/test/test_imports.py:681
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### venv/lib/python3.11/site-packages/pyflakes/test/test_api.py:398
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### backups/structure_optimization/backup_20250614_130249/scripts/security_enhancer.py:404
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### backups/structure_optimization/backup_20250614_130249/scripts/security_enhancer.py:404
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### backups/structure_optimization/backup_20250614_130249/scripts/security_enhancer.py:405
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### backups/structure_optimization/backup_20250614_130249/scripts/security_enhancer.py:407
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### backups/structure_optimization/backup_20250614_130900/scripts/security_enhancer.py:404
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### backups/structure_optimization/backup_20250614_130900/scripts/security_enhancer.py:404
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### backups/structure_optimization/backup_20250614_130900/scripts/security_enhancer.py:405
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### backups/structure_optimization/backup_20250614_130900/scripts/security_enhancer.py:407
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


### backups/structure_optimization/backup_20250614_125650/scripts/security_enhancer.py:404
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### backups/structure_optimization/backup_20250614_125650/scripts/security_enhancer.py:404
- **问题类型**: eval_usage
- **严重程度**: high
- **描述**: eval(
- **修复建议**: 避免使用eval()，考虑使用ast.literal_eval()或其他安全替代方案


### backups/structure_optimization/backup_20250614_125650/scripts/security_enhancer.py:405
- **问题类型**: exec_usage
- **严重程度**: high
- **描述**: exec(
- **修复建议**: 避免使用exec()，重新设计代码逻辑


### backups/structure_optimization/backup_20250614_125650/scripts/security_enhancer.py:407
- **问题类型**: yaml_unsafe_load
- **严重程度**: medium
- **描述**: yaml.load(
- **修复建议**: 使用yaml.safe_load()代替yaml.load()


## 配置安全问题

### venv/lib/python3.11/site-packages/cyclonedx/schema/_res/bom-1.6.SNAPSHOT.schema.json
- **问题类型**: sensitive_config
- **严重程度**: high
- **修复建议**: 将password移动到环境变量或安全的密钥管理系统


### venv/lib/python3.11/site-packages/cyclonedx/schema/_res/bom-1.6.SNAPSHOT.schema.json
- **问题类型**: sensitive_config
- **严重程度**: high
- **修复建议**: 将token移动到环境变量或安全的密钥管理系统


## 文件权限问题

### venv/bin/vba_extract.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x venv/bin/vba_extract.py


### venv/bin/runxlrd.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x venv/bin/runxlrd.py


### venv/lib/python3.11/site-packages/numpy/testing/print_coercion_tables.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x venv/lib/python3.11/site-packages/numpy/testing/print_coercion_tables.py


### backups/structure_optimization/backup_20250614_130249/scripts/deploy.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x backups/structure_optimization/backup_20250614_130249/scripts/deploy.py


### backups/structure_optimization/backup_20250614_130249/scripts/quick_enhancement.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x backups/structure_optimization/backup_20250614_130249/scripts/quick_enhancement.py


### backups/structure_optimization/backup_20250614_130900/scripts/deploy.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x backups/structure_optimization/backup_20250614_130900/scripts/deploy.py


### backups/structure_optimization/backup_20250614_130900/scripts/quick_enhancement.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x backups/structure_optimization/backup_20250614_130900/scripts/quick_enhancement.py


### backups/structure_optimization/backup_20250614_125650/scripts/deploy.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x backups/structure_optimization/backup_20250614_125650/scripts/deploy.py


### backups/structure_optimization/backup_20250614_125650/scripts/quick_enhancement.py
- **问题类型**: unnecessary_execute_permission
- **严重程度**: low
- **修复建议**: chmod -x backups/structure_optimization/backup_20250614_125650/scripts/quick_enhancement.py

