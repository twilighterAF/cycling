
const TIMER1 = document.querySelector('.timer1')
const TIMER2 = document.querySelector('.timer2')
const TIMER3 = document.querySelector('.timer3')
const TIMER4 = document.querySelector('.timer4')
const TIMER5 = document.querySelector('.timer5')


class Cycle{
  //main cycle class
  constructor(name, timerInput, id, radius){
  this.startTime = 0
  this.currentTime = 0
  this.repeats = 0
  this.name = name
  this.paused = false //
  this.started = false // 3 statuses for cycle manipulate
  this.focused = false //
  this.timer = timerInput
  this.id = id
  this.circle = document.body.querySelector('.circle' + this.id)
  this.radius = radius
  }

  pauseCycle(){
    this.paused = true
  }
  unpauseCycle(){
    this.paused = false
  }
  startCycle(){
    this.started = true
  }
  stopCycle(){
    this.started = false
  }
  focusCycle(){
    this.focused = true
  }
  unfocusCycle(){
    this.focused = false
  }


  //time input into Cycle class
  setTime(seconds){
    this.deciseconds = seconds * 10
    this.startTime = this.deciseconds
    this.currentTime = this.deciseconds
  }

  formatTime(time){
    this.totalSeconds = time/10
    const h = Math.floor(this.totalSeconds/3600)
    this.totalSeconds %= 3600
    const m = Math.floor(this.totalSeconds/60)
    this.totalSeconds %= 60
    const s = this.totalSeconds

    return this.twoDigits(h) + ':' + this.twoDigits(m) + ':' + this.twoDigits(s)
  }

  twoDigits(digit){

    if(isNaN(digit)){
    return '00'

    } else if(digit < 10){
    return "0" + digit

    } else{
    return digit.toString()
    }
  }

  //update html
  updateTimer(){
    this.timer.value = this.formatTime(this.currentTime)
  }

  //time flow generator
  *cycleGen(){
    this.deciseconds = 10
    if (this.currentTime % this.deciseconds === 0 || this.currentTime === 0){
      this.updateTimer()
    }
  
    this.currentTime--
    this.circlesUpdate()
    yield
  }

  //main timer function
  cycling(){

    if (this.currentTime > 0){
        const startCycle = setInterval(() => {
        let generator = this.cycleGen()
        generator.next()

        if (this.currentTime < 0 && this.repeats > 0){
          this.currentTime = this.startTime
          this.repeats --
        }

        else if (this.currentTime < 0 || !this.started){
          clearInterval(startCycle)
          buttonsHandler.setStartButton()
          this.stopCycle()
        }

        else if (this.paused){
          clearInterval(startCycle)
        }
      }, 100)
    }
  }

  circlesUpdate(){
    let percents = (this.currentTime / this.startTime) * 100
    let percents2 = (this.startTime / this.currentTime) * 100
    let circumference = 2 * this.radius * Math.PI
    let result = (circumference / 100 ) * percents
    this.circle.style.strokeDasharray = `${result} 5000`
  }

}


const cycle1 = new Cycle('First', TIMER1, 1, 70)
const cycle2 = new Cycle('Second', TIMER2, 2, 120)
const cycle3 = new Cycle('Third', TIMER3, 3, 170)
const cycle4 = new Cycle('Fourth', TIMER4, 4, 220)
const cycle5 = new Cycle('Fifth', TIMER5, 5, 270)

const cyclesList = [cycle1, cycle2, cycle3, cycle4, cycle5]


// object for handling input from html
const cyclesInput = {
  validateInput(cycle){
    const regExp = /([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]/g
    const inputTime = cycle.timer.value
    let validation = Boolean(inputTime.match(regExp))
    return validation
  },

  calculateInput(timeArray){
    const len = timeArray.length
    const s = Number(timeArray[len-1])
    const m = Number(timeArray[len-2]) * 60
    const h = Number(timeArray[len-3]) * 3600
    const result = s + m + h
    return result
  },

  formatInput(cycle){
    if (this.validateInput(cycle)){
      const timeArray = cycle.timer.value.split(':')
      const time = this.calculateInput(timeArray)
      return time

    }else{
      alert(`Wrong time format in cycle ${cycle.name}`)
      return '00:00:00'
    }
  },
}


const buttonsHandler = {

  setPauseButton(){
    let buttons = document.querySelectorAll('button')
    let secondButton = buttons[1]
    secondButton.className = 'pause'
    startIcon = secondButton.querySelector('i')
    startIcon.className = 'far fa-pause-circle'
  },

  setStartButton(){
    let buttons = document.querySelectorAll('button')
    let secondButton = buttons[1]
    secondButton.className = 'start'
    startIcon = secondButton.querySelector('i')
    startIcon.className = 'far fa-play-circle'
  },

  stopClick(cycle){
    cycle.stopCycle()
    cycle.currentTime = cycle.startTime
    cycle.updateTimer()
  },

  startClick(cycle){
    let time = cyclesInput.formatInput(cycle)

    if (!cycle.paused || cycle.currentTime == 0){
      cycle.setTime(time)
    }

    if (time > 0){
      cycle.unpauseCycle()
      cycle.startCycle()
      cycle.cycling()
    }
  },

  pauseClick(cycle){
    cycle.pauseCycle()
  },

  focusButtons(cycle){
    if (cycle.started && !cycle.paused){
      buttonsHandler.setPauseButton()
    }
    else{
      buttonsHandler.setStartButton()
    }
  }
}


// cycle control
const cyclesHandler = {


  cyclesPause(cyclesList){
    let focused = false

    for (let cycle of cyclesList){

      if (cycle.focused){
        focused = true
        buttonsHandler.pauseClick(cycle)
        break
      }
    }

    if (!focused){
      for (let cycle of cyclesList){
        buttonsHandler.pauseClick(cycle)
      }
    }
  },


  cyclesStop(cyclesList){
    let focused = false

    for (let cycle of cyclesList){

      if (cycle.focused){
        focused = true
        buttonsHandler.stopClick(cycle)
        break
      }
    }

    if (!focused){
      for (let cycle of cyclesList){
        buttonsHandler.stopClick(cycle)
      }
    }
  },

  cyclesStart(cyclesList){
    let focused = false

    for (let cycle of cyclesList){

      if (cycle.focused){
        focused = true
        buttonsHandler.startClick(cycle)
        break
      }
    }

    if (!focused){
      for (let cycle of cyclesList){

        if (cycle.started && !cycle.paused){
          continue
        }
        else{
          buttonsHandler.startClick(cycle)
        }
        
      }
    }
  },

  cyclesUnfocusing(cyclesList){
    for (let cycle of cyclesList){
      cycle.unfocusCycle()
      cycle.circle.removeAttribute('id')
      cycle.timer.removeAttribute('id')
    }
  },

  entry(event){
    let target = event.target

    switch(target.className){
      case 'far fa-stop-circle':
        cyclesHandler.cyclesStop(cyclesList)
        break

      case 'far fa-play-circle':
        cyclesHandler.cyclesStart(cyclesList)
        buttonsHandler.setPauseButton()
        break

      case 'far fa-pause-circle':
        cyclesHandler.cyclesPause(cyclesList)
        buttonsHandler.setStartButton()
        break
    }
  },
}


function focus(event){
  let target = event.target

  if (target instanceof HTMLInputElement){
    switch(target.className){

      case 'timer5':
        cyclesHandler.cyclesUnfocusing(cyclesList)
        cycle5.focusCycle()
        cycle5.circle.id = 'focused5'
        cycle5.timer.id = 'focused5'
        buttonsHandler.focusButtons(cycle5)
        break

      case 'timer4':
        cyclesHandler.cyclesUnfocusing(cyclesList)
        cycle4.focusCycle()
        cycle4.circle.id = 'focused4'
        cycle4.timer.id = 'focused4'
        buttonsHandler.focusButtons(cycle4)
        break

      case 'timer3':
        cyclesHandler.cyclesUnfocusing(cyclesList)
        cycle3.focusCycle()
        cycle3.circle.id = 'focused3'
        cycle3.timer.id = 'focused3'
        buttonsHandler.focusButtons(cycle3)
        break

      case 'timer2':
        cyclesHandler.cyclesUnfocusing(cyclesList)
        cycle2.focusCycle()
        cycle2.circle.id = 'focused2'
        cycle2.timer.id = 'focused2'
        buttonsHandler.focusButtons(cycle2)
        break

      case 'timer1':
        cyclesHandler.cyclesUnfocusing(cyclesList)
        cycle1.focusCycle()
        cycle1.circle.id = 'focused1'
        cycle1.timer.id = 'focused1'
        buttonsHandler.focusButtons(cycle1)
        break
    }
  }
  else if (target.className == 'wrapper'){
    cyclesHandler.cyclesUnfocusing(cyclesList)
  }
}


let BUTTONS = document.querySelector('.buttons')
BUTTONS.addEventListener('click', cyclesHandler.entry)

const BODY = document.querySelector('.wrapper')
BODY.addEventListener('click', focus)

//window.addEventListener('focus', () => console.log('focused'))
//window.addEventListener('blur', () => console.log('blurred'))