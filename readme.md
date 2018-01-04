# ⚡️ railgun

> static site generator

## Step1: Initialize a blog

```shell
$ railgun init blog
```

## Step2: Config

```shell
$ cd blog
$ vim config.py
```

don't forget to change ``default config class``
```python

config = {
    'default': MyConfig
}
```

## Step3: Writing

```shell
$ cd blog
$ railgun new newblog
```

then

```shell
$ vim app/pages/newblog.md
```

the default article template show below:

```markdown
title:
date: %Y-%m-%d %H:%M:%S
tags: ['tag1', 'tag2']
```

the default format for the blog is ``[markdown](https://guides.github.com/features/mastering-markdown/)``, you can change it in the config.py file

```python
class Config(object):
    # ......
    FLATPAGES_EXTENSION = '.md'
```

## Step4: Preview
```shell
$ railgun server
```

## Step5: Build and Deploy

```shell
$ railgun build
$ railgun upload
```

done! <br/>
enjoy writing :)

## Install

### Install from git

```shell
$ git clone https://github.com/misakar/railgun/ railgun
$ cd railgun
$ pip install --editable .
```

## Test

```shell
$ git clone https://github.com/misakar/railgun/ railgun
$ cd railgun
$ pip install --editable .
$ py.test -s
```

## More details of railgun

+ [一起写一个静态博客生成器]()

## Change Logs

### 20171231

+ back

### 20170910

+ add blog :)

### 20170907

+ add tests!

### 20170901

+ speed up! generate 200 files in just 5s :)

### 20170831

+ fix bug :(

### 20170830

+ bye bye neo1218 :) new life :(

## ToDo

+ [x] speed up
+ [x] tests
+ [ ] code high light
+ [ ] logging system
+ [ ] theme system
+ [ ] reverse generation

## CopyRight


**MIT 2018@misakar** <br/>

> check LICENSE for detail.
