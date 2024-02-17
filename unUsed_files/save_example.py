report_data = {}


@dp.message_handler(Command('report'))
async def calculate_report(message: types.Message, state: FSMContext):
    check = message.from_user.id  # проверяем доступ пользователя
    if check in config.usr_admins:
        await bot.send_message(chat_id=INFO,
                               text=f'🔑 Репорт [{message.from_user.full_name, message.from_user.id}]')

        cursor.execute("SELECT * FROM otchet")
        conn.commit()

        await message.answer(f"\n\n📊 ФОРМИРОВАНИЕ ОТЧЕТА 📊️")
        try:
            await message.answer(f'\n\n💰 В кассе остовалось : {cursor.fetchall()[-1][-3]} ₽')
        except IndexError:
            await message.answer("🪶 ТАБЛИЦА НЕ ПОДКЛЮЧЕНА 🪶")
            await bot.send_message(chat_id=INFO, text='🛑 ТАБЛИЦА НЕ ПОДКЛЮЧЕНА!!!')
            pass

        await message.answer(f'{tx.instr_1}')
        await fsm.Reports.R1.set()

    else:
        await message.answer('👨🏽‍💻 В разрабоке!')


@dp.message_handler(state=fsm.Reports.R1)
async def input_report(message: types.Message, state: FSMContext):
    try:
        money_in_the_morning = int(message.text)

    except ValueError:
        await message.answer(f'{tx.err_or_1}')
        await message.answer(f'{tx.instr_1}')
        return input_report

    await state.update_data(money_in_the_morning=money_in_the_morning)
    await message.answer(f'{tx.instr_2}')
    await fsm.Reports.R2.set()


@dp.message_handler(state=fsm.Reports.R2)
async def input_report(message: types.Message, state: FSMContext):
    try:
        proceeds = int(message.text)

    except ValueError:
        await message.answer(f'{tx.err_or_1}')
        await message.answer(f'{tx.instr_2}')
        return input_report

    await state.update_data(proceeds=proceeds)
    await message.answer(f'{tx.instr_3}')
    await fsm.Reports.R3.set()


@dp.message_handler(state=fsm.Reports.R3)
async def input_report(message: types.Message, state: FSMContext):
    try:
        cashless = int(message.text)

    except ValueError:
        await message.answer(f'{tx.err_or_1}')
        await message.answer(f'{tx.instr_3}')
        return input_report

    await state.update_data(cashless=cashless)
    await message.answer(f'{tx.instr_4}')
    await fsm.Reports.R4.set()


@dp.message_handler(state=fsm.Reports.R4)
async def input_report(message: types.Message, state: FSMContext):
    try:
        collection = int(message.text)

    except ValueError:
        await message.answer(f'{tx.err_or_1}')
        await message.answer(f'{tx.instr_4}')
        return input_report

    await state.update_data(collection=collection)
    await message.answer(f'{tx.instr_5}')
    await fsm.Reports.R5.set()


@dp.message_handler(state=fsm.Reports.R5)
async def input_report(message: types.Message, state: FSMContext):
    try:
        costs = int(message.text)

    except ValueError:
        await message.answer(f'{tx.err_or_1}')
        await message.answer(f'{tx.instr_5}')
        return input_report

    await state.update_data(costs=costs)
    await message.answer(f'{tx.instr_6}')
    await fsm.Reports.R6.set()


@dp.message_handler(state=fsm.Reports.R6)
async def input_report(message: types.Message, state: FSMContext):
    try:
        fact = int(message.text)

    except ValueError:
        await message.answer(f'{tx.err_or_1}')
        await message.answer(f'{tx.instr_6}')
        return input_report

    await state.update_data(fact=fact)
    report_data = await state.get_data()

    async def start_report(report_data):
        money_in_the_morning = int(report_data['money_in_the_morning'])
        proceeds = int(report_data['proceeds'])
        cashless = int(report_data['cashless'])
        collection = int(report_data['collection'])
        costs = int(report_data['costs'])
        fact = int(report_data['fact'])
        cash_1 = proceeds - cashless  # высчитываем наличку
        cash_2 = proceeds - cashless - collection - costs  # Остаток после инкс и доп расход
        kassa = money_in_the_morning + cash_2  # формируем кассу

        ####################################################################################################

        form = f""" 
    🗓 {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n
    🔺        ОТЧЕТ        🔻\n
    ↦ Выручка: {proceeds} ₽
    ↦ Безнал: {cashless} ₽
    ↦ Наличными: {cash_1} ₽
    ↦ Инкассации:{collection} ₽
    ↦ Доп. расходы:{costs} ₽
    ↦ Факт: {fact}₽

            """
        ####################################################################################################

        # Проверка по кассе
        if fact == kassa:

            await message.answer(f'{form}\nВ кассе: {str(kassa)}₽\nКасса ровная! シ ')

            await bot.send_message(chat_id=INFO,
                                   text=f'{form}\nВ кассе: {str(kassa)}₽\n'
                                        f'Касса ровная! シ ')


        elif fact > kassa:

            await message.answer(
                f'{form}\nВ кассе {str(fact)}₽ '
                f'\nДолжно быть {str(kassa)}₽\n'
                f'Сумма больше на {str(fact - kassa)}₽')

            await bot.send_message(chat_id=INFO,
                                   text=f'{form}\nВ кассе {str(fact)}₽ '
                                        f'\nДолжно быть {str(kassa)}₽\nСумма '
                                        f'больше на {str(fact - kassa)}₽')



        else:
            await message.answer(
                f'{form}\nВ кассе {str(fact)}₽ '
                f'\nДолжно быть {str(kassa)}₽.\n'
                f'Не хватает {str(kassa - fact)}₽')

            await bot.send_message(chat_id=INFO,
                                   text=f'{form}\nВ кассе {str(fact)}₽ '
                                        f'\nДолжно быть {str(kassa)}₽.\n'
                                        f'Не хватает {str(kassa - fact)}₽')

        priz = 9000
        difference = priz - proceeds

        if proceeds >= priz:
            await message.answer('🏆 ПРЕМИЯ 🥇:\n\nУраа... '
                                 'Вам положена премия 500₽ за '
                                 'хорошую работу! 🎊🎉🎈\n')
            await message.answer('🤑')


        elif proceeds >= priz - 1000:
            await message.answer(f'🥈 ПРЕМИЯ 🥈:\n\n🚖Вам положенно Такси в обе стороны! 🚖\n'
                                 f'До 🏆 не хватило {str(difference)} ₽  🤬 😭\n')



        elif proceeds >= priz - 2000:
            await message.answer('🥉 ПРЕМИЯ 🥉:\n\n'
                                 '🚖 Вам положенно Такси в одну сторону! 🚖\n')

        return

    await start_report(report_data)
    await state.finish()

    money_in_the_morning = int(report_data['money_in_the_morning'])
    proceeds = int(report_data['proceeds'])
    cashless = int(report_data['cashless'])
    collection = int(report_data['collection'])
    costs = int(report_data['costs'])
    fact = int(report_data['fact'])
    cash_1 = proceeds - cashless
    # высчитываем наличку,
    cash_2 = proceeds - cashless - collection - costs
    # формируем кассу
    kassa = money_in_the_morning + cash_2
    check = message.from_user.id
    user = message.from_user.username

    cursor.execute(f"INSERT INTO otchet VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}',
                    check,
                    user,
                    money_in_the_morning,
                    proceeds,
                    cashless,
                    cash_1,
                    collection,
                    costs,
                    fact,
                    kassa,
                    kassa - fact))
    conn.commit()