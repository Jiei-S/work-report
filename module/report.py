""" Make Report """
import os
import glob
import datetime
import pandas as pd
import matplotlib.pyplot as plt

TODAY = datetime.date.today().strftime('%Y年%m月%d日')
ONTIME = 460


def convert_to_minutes(hour_time):
    """ Convert to minutes

    @param hour_time: operation time(unit: hour)
    @return operation time(unit: minutes)
    """
    hour, minute = map(int, hour_time.split(':'))
    return hour*60 + minute


def calculate_overtime(operation_time):
    """ Calculate Overtime

    @param operation_time: operation time
    @return overtime
    """
    return round((convert_to_minutes(operation_time) - ONTIME)/60, 1)


def get_csv_path():
    """ Get CSV Path

    @return CSV Path
    """
    return ''.join(glob.glob('**/*.csv', recursive=True))


def extract_date_actual_work_time(work_info):
    """ Extract Work Info

    @param work_info: work info
    @return: date, actual work time
    """
    return work_info[work_info['日付形式(名称)'] == '出勤日'].loc[:, ['年月日', '実働時間']]


def format_report(work_info):
    """ Format Report

    @param work_info: work info
    @return date_actual_work_time_overtime: date, actual work time, overtime
    @return total_actual_work_time_overtime: total actual work time, total overtime
    """
    date_actual_work_time_overtime = \
        extract_date_actual_work_time(work_info).fillna('07:40').set_index('年月日')
    date_actual_work_time_overtime.loc[:, '残業時間'] = \
        work_info.loc[:, '実働時間'].apply(calculate_overtime)

    total_actual_work_time = \
        work_info.loc[:, '実働時間'].apply(convert_to_minutes).sum()

    total_actual_work_time_overtime = pd.DataFrame(
        data=[[
            round(total_actual_work_time/60, 1),
            date_actual_work_time_overtime.loc[:, '残業時間'].sum()
        ]],
        index=['合計'], columns=['実働時間', '残業時間']
    )

    return date_actual_work_time_overtime, total_actual_work_time_overtime


def make_report():
    """ Make Report

    @return True: make success
    @return False: make Failed
    """
    csv_path = get_csv_path()
    if csv_path:
        data_frame = pd.read_csv(csv_path, encoding='cp932', parse_dates=[1])
        work_info, work_sum_info = format_report(data_frame)

        plt.rcParams['font.family'] = 'IPAexGothic'
        fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=300)
        fig.suptitle(TODAY, fontsize=16)

        bbox = [0, 0, 1, 1]
        col_colours = ['#ffe6b3', '#ffe6b3']

        axs[0].axis('off')
        axs[0].table(cellText=work_info.values,
                     bbox=bbox,
                     colLabels=work_info.columns,
                     rowLabels=work_info.index,
                     colColours=col_colours)

        axs[1].axis('off')
        axs[1].table(cellText=work_sum_info.values,
                     bbox=bbox,
                     colLabels=work_sum_info.columns,
                     rowLabels=work_sum_info.index,
                     colColours=col_colours)

        plt.savefig('./module/report.png')
        os.remove(csv_path)
        return True

    return False
