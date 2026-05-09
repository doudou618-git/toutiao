from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cached_categories, get_cache_news_list, set_cache_news_list
from models.news import Category , News
from sqlalchemy import select, func, update

from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession , skip: int = 0, limit: int = 100):
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)  #查询
    result = await db.execute(stmt)   #执行
    categories =  result.scalars().all()   #提取  #这个categories是ORM对象

    #写入缓存
    if categories:
        categories = jsonable_encoder( categories)  # jsonable_encoder方法把ORM转为列表跟字典等
        await set_cached_categories(categories)
    return  categories

async def get_news_list(db: AsyncSession, category_id : int , skip: int = 0, limit: int = 10):
    #查询的是指定分类下的所有新闻
    #skip = (page - 1) * limit   page = skip/limit + 1 page = skip//limit + 1
    page = skip//limit + 1
    cached_list = await get_cache_news_list(category_id , page , limit)  #缓存数据JSON
    if cached_list:
        #缓存数据转换成ORM对象 要ORM
        return [News(**item) for item in cached_list]

    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    if news_list:
        #先把ORM数据转换为字典才能写入缓存
        # ORM先转为pydantic，再转为字典
        news_data = [NewsItemBase.model_validate( item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id , page , limit , news_data)
    return news_list

async def get_news_count(db: AsyncSession, category_id : int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()   #只能有一个结果，不然报错


async def get_news_detail(db: AsyncSession, news_id : int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id : int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    #更新 - 检查数据库是否真的命中了数据 - 命中了就返回TRUE
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id : int , category_id : int , limit: int = 5):
    #order_by 排序 - 浏览量和发布时间排序
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    #return result.scalars().all()
    related_news = result.scalars().all()
    #列表推导式 推导出新闻的核心内容 然后再return
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views
    } for news_detail in related_news]





