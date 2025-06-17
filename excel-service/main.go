package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/xuri/excelize/v2"
)

// ExcelService 提供高性能的 Excel 操作服务
type ExcelService struct {
	port string
}

// ReadRequest 读取请求结构
type ReadRequest struct {
	FilePath  string `json:"file_path" binding:"required"`
	SheetName string `json:"sheet_name,omitempty"`
	StartRow  int    `json:"start_row,omitempty"`
	EndRow    int    `json:"end_row,omitempty"`
	StartCol  string `json:"start_col,omitempty"`
	EndCol    string `json:"end_col,omitempty"`
}

// WriteRequest 写入请求结构
type WriteRequest struct {
	FilePath  string              `json:"file_path" binding:"required"`
	SheetName string              `json:"sheet_name,omitempty"`
	Data      []map[string]string `json:"data" binding:"required"`
	StartRow  int                 `json:"start_row,omitempty"`
	StartCol  string              `json:"start_col,omitempty"`
}

// ChartRequest 图表请求结构
type ChartRequest struct {
	FilePath   string `json:"file_path" binding:"required"`
	SheetName  string `json:"sheet_name,omitempty"`
	ChartType  string `json:"chart_type" binding:"required"`
	DataRange  string `json:"data_range" binding:"required"`
	Title      string `json:"title,omitempty"`
	XAxisTitle string `json:"x_axis_title,omitempty"`
	YAxisTitle string `json:"y_axis_title,omitempty"`
}

// Response 通用响应结构
type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
	Message string      `json:"message,omitempty"`
}

// NewExcelService 创建新的 Excel 服务实例
func NewExcelService(port string) *ExcelService {
	return &ExcelService{port: port}
}

// readExcel 读取 Excel 文件
func (s *ExcelService) readExcel(c *gin.Context) {
	var req ReadRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, Response{
			Success: false,
			Error:   fmt.Sprintf("Invalid request: %v", err),
		})
		return
	}

	// 验证文件是否存在
	if _, err := os.Stat(req.FilePath); os.IsNotExist(err) {
		c.JSON(http.StatusBadRequest, Response{
			Success: false,
			Error:   fmt.Sprintf("File not found: %s", req.FilePath),
		})
		return
	}

	// 打开 Excel 文件
	f, err := excelize.OpenFile(req.FilePath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to open Excel file: %v", err),
		})
		return
	}
	defer func() {
		if err := f.Close(); err != nil {
			log.Printf("Error closing file: %v", err)
		}
	}()

	// 获取工作表名称
	sheetName := req.SheetName
	if sheetName == "" {
		sheetName = f.GetSheetName(0)
	}

	// 读取数据
	rows, err := f.GetRows(sheetName)
	if err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to read sheet data: %v", err),
		})
		return
	}

	// 应用行范围过滤
	if req.StartRow > 0 || req.EndRow > 0 {
		startRow := req.StartRow
		if startRow < 1 {
			startRow = 1
		}
		endRow := req.EndRow
		if endRow <= 0 || endRow > len(rows) {
			endRow = len(rows)
		}
		if startRow <= endRow {
			rows = rows[startRow-1 : endRow]
		}
	}

	c.JSON(http.StatusOK, Response{
		Success: true,
		Data: map[string]interface{}{
			"rows":       rows,
			"sheet_name": sheetName,
			"total_rows": len(rows),
		},
		Message: "Excel file read successfully",
	})
}

// writeExcel 写入 Excel 文件
func (s *ExcelService) writeExcel(c *gin.Context) {
	var req WriteRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, Response{
			Success: false,
			Error:   fmt.Sprintf("Invalid request: %v", err),
		})
		return
	}

	// 创建新的 Excel 文件或打开现有文件
	var f *excelize.File

	if _, err := os.Stat(req.FilePath); os.IsNotExist(err) {
		// 文件不存在，创建新文件
		f = excelize.NewFile()
	} else {
		// 文件存在，打开现有文件
		var err error
		f, err = excelize.OpenFile(req.FilePath)
		if err != nil {
			c.JSON(http.StatusInternalServerError, Response{
				Success: false,
				Error:   fmt.Sprintf("Failed to open Excel file: %v", err),
			})
			return
		}
	}
	defer func() {
		if err := f.Close(); err != nil {
			log.Printf("Error closing file: %v", err)
		}
	}()

	// 获取工作表名称
	sheetName := req.SheetName
	if sheetName == "" {
		sheetName = "Sheet1"
	}

	// 确保工作表存在
	sheetIndex, _ := f.GetSheetIndex(sheetName)
	if sheetIndex < 0 {
		f.NewSheet(sheetName)
	}

	// 写入数据
	startRow := req.StartRow
	if startRow < 1 {
		startRow = 1
	}

	startCol := req.StartCol
	if startCol == "" {
		startCol = "A"
	}

	// 如果数据包含表头，先写入表头
	if len(req.Data) > 0 {
		// 获取列名
		var headers []string
		for key := range req.Data[0] {
			headers = append(headers, key)
		}

		// 写入表头
		for i, header := range headers {
			startColNum, _ := excelize.ColumnNameToNumber(startCol)
			cell, _ := excelize.CoordinatesToCellName(startColNum+i, startRow)
			f.SetCellValue(sheetName, cell, header)
		}

		// 写入数据行
		for rowIdx, rowData := range req.Data {
			for colIdx, header := range headers {
				startColNum, _ := excelize.ColumnNameToNumber(startCol)
				cell, _ := excelize.CoordinatesToCellName(startColNum+colIdx, startRow+rowIdx+1)
				f.SetCellValue(sheetName, cell, rowData[header])
			}
		}
	}

	// 保存文件
	if err := f.SaveAs(req.FilePath); err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to save Excel file: %v", err),
		})
		return
	}

	c.JSON(http.StatusOK, Response{
		Success: true,
		Data: map[string]interface{}{
			"file_path":    req.FilePath,
			"sheet_name":   sheetName,
			"rows_written": len(req.Data),
		},
		Message: "Excel file written successfully",
	})
}

// createChart 创建图表
func (s *ExcelService) createChart(c *gin.Context) {
	var req ChartRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, Response{
			Success: false,
			Error:   fmt.Sprintf("Invalid request: %v", err),
		})
		return
	}

	// 打开 Excel 文件
	f, err := excelize.OpenFile(req.FilePath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to open Excel file: %v", err),
		})
		return
	}
	defer func() {
		if err := f.Close(); err != nil {
			log.Printf("Error closing file: %v", err)
		}
	}()

	// 获取工作表名称
	sheetName := req.SheetName
	if sheetName == "" {
		sheetName = f.GetSheetName(0)
	}

	// 创建图表
	var chartType excelize.ChartType
	switch req.ChartType {
	case "col":
		chartType = excelize.Col
	case "line":
		chartType = excelize.Line
	case "pie":
		chartType = excelize.Pie
	default:
		chartType = excelize.Col
	}

	if err := f.AddChart(sheetName, "E1", &excelize.Chart{
		Type: chartType,
		Series: []excelize.ChartSeries{{
			Name:       req.Title,
			Categories: req.DataRange,
			Values:     req.DataRange,
		}},
		Title: []excelize.RichTextRun{{
			Text: req.Title,
		}},
		PlotArea: excelize.ChartPlotArea{
			ShowCatName:     false,
			ShowLeaderLines: false,
			ShowPercent:     true,
			ShowSerName:     true,
			ShowVal:         true,
		},
	}); err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to create chart: %v", err),
		})
		return
	}

	// 保存文件
	if err := f.Save(); err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to save Excel file: %v", err),
		})
		return
	}

	c.JSON(http.StatusOK, Response{
		Success: true,
		Data: map[string]interface{}{
			"file_path":  req.FilePath,
			"sheet_name": sheetName,
			"chart_type": req.ChartType,
		},
		Message: "Chart created successfully",
	})
}

// getFileInfo 获取文件信息
func (s *ExcelService) getFileInfo(c *gin.Context) {
	filePath := c.Query("file_path")
	if filePath == "" {
		c.JSON(http.StatusBadRequest, Response{
			Success: false,
			Error:   "file_path parameter is required",
		})
		return
	}

	// 验证文件是否存在
	fileInfo, err := os.Stat(filePath)
	if os.IsNotExist(err) {
		c.JSON(http.StatusBadRequest, Response{
			Success: false,
			Error:   fmt.Sprintf("File not found: %s", filePath),
		})
		return
	}

	// 打开 Excel 文件
	f, err := excelize.OpenFile(filePath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, Response{
			Success: false,
			Error:   fmt.Sprintf("Failed to open Excel file: %v", err),
		})
		return
	}
	defer func() {
		if err := f.Close(); err != nil {
			log.Printf("Error closing file: %v", err)
		}
	}()

	// 获取工作表信息
	sheetList := f.GetSheetList()
	sheetInfo := make(map[string]interface{})
	totalMergedCells := 0
	sheetsWithMultiHeaders := 0
	complexStructureDetected := false

	for _, sheetName := range sheetList {
		rows, _ := f.GetRows(sheetName)

		// 分析合并单元格
		mergedCells, _ := f.GetMergeCells(sheetName)
		mergedCellsInfo := make([]map[string]interface{}, 0)
		for _, mergeCell := range mergedCells {
			// 解析合并单元格范围
			startCol, startRow, _ := excelize.CellNameToCoordinates(mergeCell.GetStartAxis())
			endCol, endRow, _ := excelize.CellNameToCoordinates(mergeCell.GetEndAxis())

			mergedCellsInfo = append(mergedCellsInfo, map[string]interface{}{
				"range":     fmt.Sprintf("%s:%s", mergeCell.GetStartAxis(), mergeCell.GetEndAxis()),
				"start_row": startRow,
				"end_row":   endRow,
				"start_col": startCol,
				"end_col":   endCol,
				"span_rows": endRow - startRow + 1,
				"span_cols": endCol - startCol + 1,
			})

			// 限制返回前10个合并单元格
			if len(mergedCellsInfo) >= 10 {
				break
			}
		}
		totalMergedCells += len(mergedCells)

		// 简单的多级表头检测逻辑
		multiHeaderDetected := false
		headerCandidates := make([]int, 0)
		structureType := "single_level"
		confidence := 0.0

		// 检测前几行是否可能是表头
		if len(rows) > 1 {
			// 检查前5行的内容特征
			maxCheckRows := 5
			if len(rows) < maxCheckRows {
				maxCheckRows = len(rows)
			}

			for i := 0; i < maxCheckRows; i++ {
				if len(rows[i]) > 0 {
					// 计算非空单元格数量
					nonEmptyCount := 0
					textCount := 0

					for _, cell := range rows[i] {
						if cell != "" {
							nonEmptyCount++
							// 简单判断是否为文本（非纯数字）
							if _, err := strconv.ParseFloat(cell, 64); err != nil {
								textCount++
							}
						}
					}

					// 如果文本比例高且非空单元格适中，可能是表头
					if nonEmptyCount > 1 && textCount > nonEmptyCount/2 {
						headerCandidates = append(headerCandidates, i+1) // 转换为1基索引
					}
				}
			}

			// 如果有多个表头候选行，可能是多级表头
			if len(headerCandidates) > 1 {
				// 检查是否有相邻的候选行
				for i := 0; i < len(headerCandidates)-1; i++ {
					if headerCandidates[i+1]-headerCandidates[i] <= 2 {
						multiHeaderDetected = true
						structureType = "multi_level"
						confidence = 0.7
						break
					}
				}
			}

			// 如果检测到合并单元格在前几行，增加多级表头的可能性
			if len(mergedCells) > 0 {
				for _, mergeCell := range mergedCells {
					_, startRow, _ := excelize.CellNameToCoordinates(mergeCell.GetStartAxis())
					if startRow <= 3 { // 前3行有合并单元格
						multiHeaderDetected = true
						structureType = "merged_header"
						confidence = 0.8
						break
					}
				}
			}
		}

		if multiHeaderDetected {
			sheetsWithMultiHeaders++
			complexStructureDetected = true
		}

		if len(mergedCells) > 0 {
			complexStructureDetected = true
		}

		// 构建工作表信息
		sheetInfo[sheetName] = map[string]interface{}{
			"row_count": len(rows),
			"col_count": func() int {
				if len(rows) > 0 {
					return len(rows[0])
				}
				return 0
			}(),
			"has_data": len(rows) > 0,
			// 新增：多级表头信息
			"multi_level_header": map[string]interface{}{
				"detected":          multiHeaderDetected,
				"structure_type":    structureType,
				"confidence":        confidence,
				"header_candidates": headerCandidates,
			},
			// 新增：合并单元格信息
			"merged_cells": map[string]interface{}{
				"count":  len(mergedCells),
				"ranges": mergedCellsInfo,
			},
		}
	}

	c.JSON(http.StatusOK, Response{
		Success: true,
		Data: map[string]interface{}{
			"file_name":     filepath.Base(filePath),
			"file_size":     fileInfo.Size(),
			"modified_time": fileInfo.ModTime(),
			"sheet_count":   len(sheetList),
			"sheets":        sheetInfo,
			// 新增：整体文件结构分析
			"file_structure_summary": map[string]interface{}{
				"total_merged_cells":         totalMergedCells,
				"sheets_with_multi_headers":  sheetsWithMultiHeaders,
				"complex_structure_detected": complexStructureDetected,
			},
		},
		Message: "Enhanced file info retrieved successfully with structure analysis",
	})
}

// health 健康检查
func (s *ExcelService) health(c *gin.Context) {
	c.JSON(http.StatusOK, Response{
		Success: true,
		Data: map[string]interface{}{
			"status":  "healthy",
			"service": "excel-service",
			"version": "1.0.0",
		},
		Message: "Service is running",
	})
}

// setupRoutes 设置路由
func (s *ExcelService) setupRoutes() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// 添加 CORS 中间件
	r.Use(func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})

	// API 路由
	api := r.Group("/api/v1")
	{
		api.GET("/health", s.health)
		api.GET("/file-info", s.getFileInfo)
		api.POST("/read", s.readExcel)
		api.POST("/write", s.writeExcel)
		api.POST("/chart", s.createChart)
	}

	return r
}

// Start 启动服务
func (s *ExcelService) Start() error {
	r := s.setupRoutes()
	log.Printf("Excel Service starting on port %s", s.port)
	return r.Run(":" + s.port)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	service := NewExcelService(port)
	if err := service.Start(); err != nil {
		log.Fatal("Failed to start service:", err)
	}
}
