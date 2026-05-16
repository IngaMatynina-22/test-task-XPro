from decimal import Decimal

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.models import Category
from src.database import AsyncSessionLocal
from src.product.models import Product, ProductAttribute, ProductCategory, ProductImage


async def seed_database() -> None:
    async with AsyncSessionLocal() as db:
        await clear_database(db)

        biker = Category(
            name="Для мотоцикліста",
            description="Товари для мотоциклістів.",
            parent_category_id=None,
            seo_keyword="dlya-motocyklista",
            meta_title="Для мотоцикліста",
            meta_description="Все для мотоцикліста.",
            meta_keyword="мотоцикліст, екіпірування",
            image="/images/categories/biker.jpg",
            status=1,
        )
        motorcycle = Category(
            name="Для мотоцикла",
            description="Товари для мотоцикла.",
            parent_category_id=None,
            seo_keyword="dlya-motocykla",
            meta_title="Для мотоцикла",
            meta_description="Все для мотоцикла.",
            meta_keyword="мотоцикл, аксесуари",
            image="/images/categories/motorcycle.jpg",
            status=1,
        )

        db.add_all([biker, motorcycle])
        await db.flush()

        accessories = Category(
            name="Аксесуари",
            parent_category_id=biker.category_id,
            seo_keyword="aksesuary",
            meta_title="Аксесуари",
            meta_description="Аксесуари для мотоцикліста.",
            meta_keyword="аксесуари, мото",
            image="/images/categories/accessories.jpg",
            status=1,
        )
        shoes = Category(
            name="Взуття",
            parent_category_id=biker.category_id,
            seo_keyword="vzuttia",
            meta_title="Мотовзуття",
            meta_description="Взуття для мотоциклістів.",
            meta_keyword="мотовзуття, взуття",
            image="/images/categories/shoes.jpg",
            status=1,
        )
        bestseller = Category(
            name="Бестселери",
            parent_category_id=biker.category_id,
            seo_keyword="bestselery",
            meta_title="Бестселери",
            meta_description="Популярні товари.",
            meta_keyword="бестселери",
            image="/images/categories/bestsellers.jpg",
            status=0,
        )

        db.add_all([accessories, shoes, bestseller])
        await db.flush()

        backpacks = Category(
            name="Рюкзаки",
            parent_category_id=accessories.category_id,
            seo_keyword="rukzaky",
            meta_title="Рюкзаки",
            meta_description="Моторюкзаки.",
            meta_keyword="рюкзаки, мото",
            image="/images/categories/backpacks.jpg",
            status=1,
        )
        balaclavas = Category(
            name="Балаклави та коміри",
            parent_category_id=accessories.category_id,
            seo_keyword="balaklavy-ta-komiry",
            meta_title="Балаклави та коміри",
            meta_description="Балаклави та коміри для мотоциклістів.",
            meta_keyword="балаклави, коміри",
            image="/images/categories/balaclavas.jpg",
            status=1,
        )
        knee_pads = Category(
            name="Накладки на коліна",
            parent_category_id=accessories.category_id,
            seo_keyword="nakladky-na-kolina",
            meta_title="Накладки на коліна",
            meta_description="Захист колін.",
            meta_keyword="коліна, захист",
            image="/images/categories/knee-pads.jpg",
            status=1,
        )
        short_shoes = Category(
            name="Короткі",
            parent_category_id=shoes.category_id,
            seo_keyword="korotki",
            meta_title="Короткі мотоботи",
            meta_description="Коротке мотовзуття.",
            meta_keyword="короткі, мотоботи",
            image="/images/categories/short-boots.jpg",
            status=1,
        )
        adventure_shoes = Category(
            name="Пригоди",
            parent_category_id=shoes.category_id,
            seo_keyword="pryhody",
            meta_title="Пригодницьке взуття",
            meta_description="Взуття для пригод.",
            meta_keyword="пригоди, мотоботи",
            image="/images/categories/adventure-boots.jpg",
            status=1,
        )

        db.add_all([backpacks, balaclavas, knee_pads, short_shoes, adventure_shoes])
        await db.flush()

        helmet = Product(
            name="Мотошолом LS2 FF800",
            description="Спортивний мотошолом для міста та траси.",
            seo_keyword="motosholom-ls2-ff800",
            meta_title="Мотошолом LS2 FF800",
            meta_description="Купити мотошолом LS2 FF800.",
            meta_keyword="шолом, мото, ls2",
            image="/images/products/helmet-main.jpg",
            status=1,
            price=Decimal("3499.99"),
            model="LS2-FF800",
            manufacturer_id=101,
            rating=4.8,
            viewed=152,
        )
        backpack = Product(
            name="Моторюкзак Alpinestars City Hunter",
            description="Зручний рюкзак для щоденних поїздок.",
            seo_keyword="motorukzak-alpinestars-city-hunter",
            meta_title="Моторюкзак Alpinestars",
            meta_description="Купити моторюкзак Alpinestars.",
            meta_keyword="рюкзак, alpinestars, мото",
            image="/images/products/backpack-main.jpg",
            status=1,
            price=Decimal("2299.00"),
            model="CITY-HUNTER",
            manufacturer_id=102,
            rating=4.6,
            viewed=98,
        )
        boots = Product(
            name="Мотоботи Adventure Pro",
            description="Туристичні мотоботи для дальніх подорожей.",
            seo_keyword="motoboty-adventure-pro",
            meta_title="Мотоботи Adventure Pro",
            meta_description="Купити мотоботи Adventure Pro.",
            meta_keyword="мотоботи, adventure",
            image="/images/products/boots-main.jpg",
            status=1,
            price=Decimal("4999.50"),
            model="ADV-PRO",
            manufacturer_id=103,
            rating=4.9,
            viewed=74,
        )
        balaclava = Product(
            name="Балаклава Thermo Moto",
            description="Тепла балаклава під шолом.",
            seo_keyword="balaklava-thermo-moto",
            meta_title="Балаклава Thermo Moto",
            meta_description="Купити балаклаву для мотоцикліста.",
            meta_keyword="балаклава, thermo, moto",
            image="/images/products/balaclava-main.jpg",
            status=0,
            price=Decimal("399.99"),
            model="THERMO-MOTO",
            manufacturer_id=104,
            rating=4.2,
            viewed=31,
        )

        db.add_all([helmet, backpack, boots, balaclava])
        await db.flush()

        db.add_all(
            [
                ProductCategory(product_id=helmet.product_id, category_id=bestseller.category_id),
                ProductCategory(product_id=helmet.product_id, category_id=accessories.category_id),
                ProductCategory(product_id=backpack.product_id, category_id=backpacks.category_id),
                ProductCategory(product_id=boots.product_id, category_id=adventure_shoes.category_id),
                ProductCategory(product_id=balaclava.product_id, category_id=balaclavas.category_id),
            ]
        )

        db.add_all(
            [
                ProductImage(product_id=helmet.product_id, image="/images/products/helmet-1.jpg", sort_order=0),
                ProductImage(product_id=helmet.product_id, image="/images/products/helmet-2.jpg", sort_order=1),
                ProductImage(product_id=backpack.product_id, image="/images/products/backpack-1.jpg", sort_order=0),
                ProductImage(product_id=backpack.product_id, image="/images/products/backpack-2.jpg", sort_order=1),
                ProductImage(product_id=boots.product_id, image="/images/products/boots-1.jpg", sort_order=0),
                ProductImage(product_id=balaclava.product_id, image="/images/products/balaclava-1.jpg", sort_order=0),
            ]
        )

        db.add_all(
            [
                ProductAttribute(
                    product_id=helmet.product_id,
                    group_name="Основні характеристики",
                    name="Матеріал",
                    value="Полікарбонат",
                    sort_order=0,
                ),
                ProductAttribute(
                    product_id=helmet.product_id,
                    group_name="Основні характеристики",
                    name="Розмір",
                    value="L",
                    sort_order=1,
                ),
                ProductAttribute(
                    product_id=backpack.product_id,
                    group_name="Характеристики",
                    name="Обʼєм",
                    value="25 л",
                    sort_order=0,
                ),
                ProductAttribute(
                    product_id=backpack.product_id,
                    group_name="Характеристики",
                    name="Матеріал",
                    value="Поліестер",
                    sort_order=1,
                ),
                ProductAttribute(
                    product_id=boots.product_id,
                    group_name="Характеристики",
                    name="Сезон",
                    value="Всесезонні",
                    sort_order=0,
                ),
                ProductAttribute(
                    product_id=boots.product_id,
                    group_name="Характеристики",
                    name="Захист",
                    value="Посилений носок та пʼята",
                    sort_order=1,
                ),
                ProductAttribute(
                    product_id=balaclava.product_id,
                    group_name="Характеристики",
                    name="Матеріал",
                    value="Фліс",
                    sort_order=0,
                ),
            ]
        )

        await db.commit()
        print("Database seeded successfully")


async def clear_database(db: AsyncSession) -> None:
    await db.execute(delete(ProductAttribute))
    await db.execute(delete(ProductImage))
    await db.execute(delete(ProductCategory))
    await db.execute(delete(Product))
    await db.execute(delete(Category))
    await db.commit()