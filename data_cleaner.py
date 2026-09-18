import pandas as pd 
import numpy as np 
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

class DataCleaner:
    def __init__(self, file_path: str):
        # khởi tạo class DataCleaner với đường dẫn tệp dữ liệu
        self.file_path = file_path
        self.data = None

    def load_data(self) -> pd.DataFrame:
        # đọc dữ liệu từ CSV và lưu vào biến self.data
        try:
            self.df = pd.read_csv(self.file_path)
            print("Dữ liệu đã được tải thành công từ:", self.file_path)
            return self.df
        except FileNotFoundError:
            print("Không tìm thấy tệp:", self.file_path)
            return None 

    def inspect_data(self):
        # kiểm tra thông tin cơ bản về dữ liệu
        if self.df is None:
            print("Dữ liệu chưa được tải. Vui lòng gọi load_data() trước!")
            return

        print("1. Thông tin dữ liệu:")
        print(self.df.info())
        print(f"\n2. Số lượng cột: {self.df.shape[1]}")
        print(f"\n3. Số lượng hàng: {self.df.shape[0]}")
        print("\n4. Kiểu dữ liệu của các cột: ")
        print(self.df.dtypes)
        print("\n5. Số lượng giá trị thiếu: ")
        print(self.df.isnull().sum())
        print(f"\n6. Số lượng giá trị trùng lặp:")
        print(self.df.duplicated().sum())
        print("\n7. Thống kê mô tả cho các cột số: ")
        print(self.df.describe())
        print("\n8. Xem trước 10 dòng đầu tiên của dữ liệu: ")
        print(self.df.head(10))



    def clean_data(self) -> pd.DataFrame:
        if self.df is None:
            print("Dữ liệu chưa được tải. Vui lòng gọi load_data() trước!")
            return None
        print("Bắt đầu quá trình làm sạch dữ liệu...")

        # đổi tên cột unnamed: 0 thành students_ID
        if 'Unnamed: 0' in self.df.columns:
            self.df.rename(columns = {'Unnamed: 0': 'students_ID'}, inplace=True)
            print("Đã đổi tên cột 'Unnamed: 0' thành 'students_ID'.")
            
        # xóa khoảng trắng ở tên cột 
        string_cols = self.df.select_dtypes(include=['object','string']).columns
        for col in string_cols:
            self.df[col] = self.df[col].astype(str).str.strip()
        print("Đã xóa khoảng trắng ở tên cột.")
     

        # đảm bảo các cột chi tiêu/ thu nhập không có giá trị âm
        numeric_cols = self.df.select_dtypes(include=['int64','float64']).columns
        for col in numeric_cols:
            if col != 'students_ID':
                self.df[col] = self.df[col].apply(lambda x: max(x, 0))
        print("Đã đảm bảo các cột chi tiêu/ thu nhập không có giá trị âm.")
        return self.df

    def save_cleaned_data(self, output_path: str = "cleaned_student_spending.csv"):
        """Bước cuối: Xuất dữ liệu đã làm sạch ra file CSV mới"""
        if self.df is not None:
            self.df.to_csv(output_path, index=False)
            print(f"Đã lưu thành công file dữ liệu sạch: '{output_path}'")
        else:
            print("Không có dữ liệu để lưu!")
            
    def convert_usd_to_vnd(self, exchange_rate: float = 25000) -> pd.DataFrame:
        """Quy đổi các cột chi tiêu/thu nhập từ USD sang VND"""
        if self.df is None:
            print("Dữ liệu chưa được tải. Vui lòng gọi load_data() trước!")
            return None

        # Lấy danh sách các cột số (loại trừ cột ID)
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        cols_to_convert = [col for col in numeric_cols if col != 'students_ID']

        # Nhẩm nhân tỷ giá cho từng cột số
        for col in cols_to_convert:
            self.df[col] = self.df[col] * exchange_rate

        print(f"Đã chuyển đổi toàn bộ dữ liệu từ USD sang VND (Tỷ giá: 1 USD = {exchange_rate:,.0f} VND).")
        return self.df
    
        
if __name__ == "__main__":
    # Khai báo và nạp file
    cleaner = DataCleaner("student_spending (1).csv")
    
    if cleaner.load_data() is not None:
        # Bước 1: Khảo sát
        cleaner.inspect_data()
        
        # Bước 3: Làm sạch
        cleaner.clean_data()
        
        # Bước 4: Chuyển đổi sang VND (Bổ sung bước này)
        cleaner.convert_usd_to_vnd(exchange_rate=25000)
        
        # Bước cuối: Xuất file CSV sạch
        cleaner.save_cleaned_data()

        print("\n XEM THỬ BẢNG DỮ LIỆU MỚI ĐÃ LÀM SẠCH (5 DÒNG ĐẦU):")
        print(cleaner.df.head())
