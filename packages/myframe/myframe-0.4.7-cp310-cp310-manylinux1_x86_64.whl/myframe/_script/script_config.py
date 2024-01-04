import click
import string


@click.command()
@click.argument('project_name')
def main(project_name: str = "TEST"):
    """配置生成

    注册为myframe.config命令，指定project_name初始配置

    Usage:
        >>> myframe._script.config project-name

    """

    project_name = project_name.lower().replace("-", "_").replace(" ", "_")
    project_prefix = project_name.upper()
    pat = string.Template("""{
  "${project_prefix}__PROJECT__NAME": "${project_name}",    
  "${project_prefix}__ENV": "DEV",    
  "${project_prefix}__TYPE": "package",
  "${project_prefix}__VERSION": "0.1.0",  
  "${project_prefix}__API__PORT": 20001,
  "${project_prefix}__API__PREFIX": "/prefix",
  "${project_prefix}__API__WORKERS": 4,
  "${project_prefix}__LOG__LEVEL": "DEBUG",
  "${project_prefix}__LOG__COLUMN_CONTEXTVAR": "traceid,path",
  "${project_prefix}__LOG__COLUMN_MSG": "traceid",
  "${project_prefix}__SERVICES": 
  [
    {
      "name": "database_service_name",
      "type": "mysql",
      "info": 
      {
        "user": "user",
        "password": "password",
        "host": "ip",
        "port": 3306,
        "db": "dbname"
      }
    },
    {
      "name": "redis_service_name",
      "type": "redis",
      "info":
      {
        "password": "password",
        "host":"192.168.1.104",
        "port": 6379,
        "db": 0
      }
    },
    {
      "name": "http_service_name",
      "type": "http_client",
      "info":
      {
        "address":"127.0.0.1:18004"
      }
    },
    {
      "name": "service_jwt",
      "type": "jwt",
      "info": {
        "secret_key": "9b9ff4eaca2cd11713a72e91719435b3b8017a65",
        "timeout": 14400
      }
    }
  ],
  "${project_prefix}__OTHER": {}
}""")
    rst = pat.substitute(project_prefix=project_prefix, project_name=project_name)
    with open(f"{project_name}-config.json", "w", encoding='utf-8') as f:
        f.write(rst)

if __name__ == "__main__":
    main()
