ARG Flink_Vesion
FROM flink:${Flink_Vesion}
RUN rm -f /etc/localtime && ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN export LANG=zh_CN.UTF-8

# 创建用户和用户组，跟yaml编排里的user: 10000:10000
RUN groupadd --system --gid=10000 hadoop && useradd --system --home-dir /home/hadoop --uid=10000 --gid=hadoop hadoop -m

# 给hadoop添加sudo权限
RUN echo "hadoop ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN mkdir /opt/apache

ADD hadoop-3.3.5.tar.gz  /opt/apache

RUN ln -s /opt/apache/hadoop-3.3.5 /opt/apache/hadoop

ENV HADOOP_HOME /opt/apache/hadoop
ENV PATH=$HADOOP_HOME/bin/:$PATH

RUN chown -R hadoop:hadoop /opt/